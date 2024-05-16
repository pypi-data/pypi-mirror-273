import json
from python_grains.profiles.exceptions import InvalidQuery, InvalidAudienceConfiguration

DEFAULT_REDIS_CLIENT = None
DEFAULT_DJANGO_AUDIENCE_MODEL = None
DEFAULT_DJANGO_CONNECTION_TUPLE = (None, None)
DEFAULT_DJANGO_MAX_FUNC = None
DEFAULT_AUDIENCE_TTL = 14 * 24 * 60 * 60
DEFAULT_AUDIENCE_DOMAINS = []
DEFAULT_DOMAIN = None
DEFAULT_AUDIENCE_ID_PREFIX = 'hic_au_'
DEFAULT_ALLOWED_FIELD_TYPES = {
    'int': {
        'ops': ['$gt', '$lt', '$eq'],
        'validate': lambda x: isinstance(x, int)
    },
    'str': {
        'ops': ['$eq'],
        'validate': lambda x: isinstance(x, str)
    },
    'bool': {
        'ops': ['$eq'],
        'validate': lambda x: isinstance(x, bool)
    },
    'list': {
        'ops': ['$contains'],
        'validate': lambda x: isinstance(x, str)}
}

DEFAULT_ALLOWED_AUDIENCE_FIELDS = {}

class QueryAtom(object):

    def __init__(self,
                 var,
                 value,
                 operator,
                 allowed_fields):

        self.var = var
        self.value = value
        self.operator = operator
        self.allowed_fields = allowed_fields
        self.validate()


    def validate(self):

        if self.var.startswith('$'):
            raise InvalidQuery(f'No operator allowed here: `{self.var}`')

        if not self.var in self.allowed_fields:
            raise InvalidQuery(f'Unknown field `{self.var}`')

        if not self.operator in DEFAULT_ALLOWED_FIELD_TYPES[self.allowed_fields[self.var]['type']]['ops']:
            raise InvalidQuery(f'Invalid operator here: `{self.operator}` @ `{self.var}`')

        if not DEFAULT_ALLOWED_FIELD_TYPES[self.allowed_fields[self.var]['type']]['validate'](self.value):
            raise InvalidQuery(f'Invalid value type for `{self.var}`, must be {self.allowed_fields[self.var]["type"]}')

    def run(self,
            value):

        if value is None:
            return False

        if self.operator == '$eq':
            return value == self.value

        elif self.operator == '$gt':
            return value > self.value

        elif self.operator == '$lt':
            return value < self.value

        elif self.operator == '$contains':
            return self.value in value

        else:
            raise InvalidQuery(f'Operator not implemented: {self.operator}')


class AudienceQuery(object):

    def __init__(self,
                 query,
                 allowed_fields,
                 op_c1=None,
                 name=None,
                 au_id=None,
                 raw_query=None,
                 valid_query=True):

        self.allowed_fields = allowed_fields
        self.op_c1 = op_c1
        self.query = query
        self.name = name
        self.au_id = au_id
        self.raw_query = raw_query
        self.valid_query = valid_query

    @classmethod
    def from_raw_data(cls,
                      raw_data,
                      allowed_fields,
                      op_c1=None,
                      name=None,
                      raise_invalid_query=False):

        query_data = raw_data['query']
        au_id = raw_data['au_id']
        try:
            query = cls.parse(query_data, allowed_fields=allowed_fields)
        except InvalidQuery as e:
            if raise_invalid_query:
                raise e
            return cls(query=None,
                       au_id=au_id,
                       op_c1=op_c1,
                       name=name,
                       raw_query=query_data,
                       allowed_fields=allowed_fields,
                       valid_query=False)

        return cls(query=query,
                   au_id=au_id,
                   op_c1=op_c1,
                   name=name,
                   raw_query=query_data,
                   allowed_fields=allowed_fields)

    @classmethod
    def parse_c1_operator_argument(cls,
                                   operator,
                                   argument,
                                   allowed_fields):

        if operator in ('$or', '$and',):

            if not isinstance(argument, list):
                raise InvalidQuery(f'The `{operator}` operator expects a list')

            query = cls.parse(argument, allowed_fields=allowed_fields)

            return AudienceQuery(query, op_c1=operator, allowed_fields=allowed_fields)

        elif operator in ('$not',):

            if not isinstance(argument, dict):
                raise InvalidQuery(f'The `{operator}` operator expects a dictionary')

        else:
            raise InvalidQuery(f'Unknown operator {operator}')

    @classmethod
    def parse_query_atom(cls,
                         field_name,
                         value,
                         allowed_fields):

        if isinstance(value, (bool, int, float, str)):
            return QueryAtom(var=field_name, value=value, operator='$eq', allowed_fields=allowed_fields)

        elif isinstance(value, dict):
            if len(value) != 1:
                raise InvalidQuery(f'Invalid query for {field_name}')
            return QueryAtom(var=field_name,
                             value=list(value.values())[0],
                             operator=list(value.keys())[0],
                             allowed_fields=allowed_fields)

        else:
            raise InvalidQuery(f'Invalid entry at `{field_name}`')

    @classmethod
    def parse(cls,
              raw_data,
              allowed_fields):

        '''
        A recursive function that parses the audience query. It raises an InvalidQuery exception if
        the query is invalid. It returns an array with the parsed query when successful.
        '''

        parts = []

        if len(raw_data) == 0:
            raise InvalidQuery('Empty query is not allowed')

        if isinstance(raw_data, dict):

            for kw, v in raw_data.items():

                if kw.startswith('$'):

                    parts.append(cls.parse_c1_operator_argument(operator=kw, argument=v, allowed_fields=allowed_fields))

                else:

                    parts.append(cls.parse_query_atom(field_name=kw, value=v, allowed_fields=allowed_fields))

        elif isinstance(raw_data, list):

            for el in raw_data:
                parts.extend(cls.parse(el, allowed_fields=allowed_fields))

        else:
            raise InvalidQuery('Query needs to be a list or a dictionary.')

        return parts

    def run(self, data):

        if not self.valid_query:
            return False

        res = []

        for part in self.query:

            if isinstance(part, AudienceQuery):
                res.append(part.run(data))

            elif isinstance(part, QueryAtom):
                res.append(part.run(data.get(part.var)))

            else:
                raise InvalidQuery(f'Invalid query part of type {type(part)}')

        if not self.op_c1 is None and self.op_c1 == '$or':
            return any(res)

        elif not self.op_c1 is None and self.op_c1 == '$not':
            return not all(res)

        elif not self.op_c1 is None and self.op_c1 == '$and':
            return all(res)

        else:
            return all(res)


class Audiences(object):

    django_audience_model = DEFAULT_DJANGO_AUDIENCE_MODEL
    django_connection_tuple = DEFAULT_DJANGO_CONNECTION_TUPLE
    django_max_func = DEFAULT_DJANGO_MAX_FUNC
    audience_ttl = DEFAULT_AUDIENCE_TTL
    redis_client = DEFAULT_REDIS_CLIENT
    domain = DEFAULT_DOMAIN
    audience_domains = DEFAULT_AUDIENCE_DOMAINS
    default_audience_id_prefix = DEFAULT_AUDIENCE_ID_PREFIX
    allowed_field_types = DEFAULT_ALLOWED_FIELD_TYPES

    def __init__(self,
                 au_domain=None,
                 force_db_init=False,
                 allowed_audience_fields=None):

        self.au_domain = au_domain or '_global'
        self.queries = self.get_queries(force_db=force_db_init)
        self.allowed_audience_fields = allowed_audience_fields or {}

    def add(self,
            query,
            name='',
            description='',
            active=True,
            id_prefix=None,
            id_num=None):

        AudienceQuery.parse(query, self.allowed_audience_fields)

        id_prefix = id_prefix or self.default_audience_id_prefix

        if id_num is None:
            q = self.django_audience_model.objects.filter(id_prefix=id_prefix).aggregate(self.django_max_func('id_num'))
            id_num_max = q['id_num__max']

            if id_num_max is None:
                id_num_max = 0
            id_num = id_num_max + 1

        audience = self.django_audience_model(
            id_num=id_num,
            id_prefix=id_prefix,
            query=json.dumps(query),
            name=name,
            description=description,
            active=active,
            domain=self.au_domain)

        audience.save()
        self.build_cache()
        return audience

    def run(self,
            data):
        parsed_data = self.parse_profile_data(data=data)
        return [query.au_id for query in self.queries if query.run(parsed_data)]

    def parse_profile_data(self,
                           data):
        parsed = {}

        for field_name, specs in self.allowed_audience_fields.items():
            if specs['type'] in self.allowed_field_types:
                value = (data.get(specs['propType']) or {}).get(field_name)
                parsed[field_name] = value

        return parsed


    @classmethod
    def parse_query(cls, query, allowed_audience_fields):
        AudienceQuery.parse(raw_data=query, allowed_fields=allowed_audience_fields)

    @classmethod
    def n_active(cls, au_domain):
        return cls.django_audience_model.objects.filter(domain=au_domain, active=True).count()

    @classmethod
    def list(cls, au_domain=None):

        if au_domain is None:
            audiences = [audience.repr_data for audience in cls.django_audience_model.objects.all()]
        else:
            audiences = [audience.repr_data for audience in cls.django_audience_model.objects.filter(domain=au_domain)]
            if not au_domain == '_global':
                audiences.extend(
                    [audience.repr_data for audience in cls.django_audience_model.objects.filter(domain='_global')])

        return audiences

    def get_queries(self,
                    force_db=False):

        if not force_db:
            audience_queries, raw_data = self.get_queries_from_cache()
        else:
            audience_queries, raw_data = None, None

        if audience_queries is None:

            audience_queries, raw_data = self.get_queries_from_db(au_domain=self.au_domain,
                                                                  allowed_audience_fields=self.allowed_audience_fields)

            if audience_queries is None:
                InvalidAudienceConfiguration('No valid audiences configuration found.')

            self.queries_to_cache(raw_data)

        return audience_queries

    def get_queries_from_cache(self):

        audiences = self.redis_client.get(self.cache_audiences_key)

        if not audiences is None:
            data = json.loads(audiences.decode())
            return [AudienceQuery.from_raw_data(raw_data=d, allowed_fields=self.allowed_audience_fields) for d in data], data
        else:
            return None, None

    @classmethod
    def get(cls,
            audience_id_prefix,
            audience_id_num):

        try:
            obj = cls.django_audience_model.objects.get(id_num=audience_id_num,
                                                        id_prefix=audience_id_prefix)
            return obj

        except cls.django_audience_model.DoesNotExist:

            return None

    @classmethod
    def get_queries_from_db(cls, au_domain, allowed_audience_fields, active=True):

        data = [a.short_data for a in cls.django_audience_model.objects.filter(active=active, domain=au_domain)]

        if not au_domain == '_global':
            data.extend([a.short_data for a in cls.django_audience_model.objects.filter(active=active, domain='_global')])

        audience_queries = [AudienceQuery.from_raw_data(raw_data=d, allowed_fields=allowed_audience_fields) for d in data]

        return audience_queries, data

    def queries_to_cache(self,
                         audience_data):

        self._queries_to_cache(au_domain=self.au_domain, audience_data=audience_data)

    @classmethod
    def _queries_to_cache(cls,
                          au_domain,
                          audience_data):

        cls.redis_client.set(cls._cache_audiences_key(au_domain=au_domain), json.dumps(audience_data),
                             ex=cls.audience_ttl)

    def build_cache(self):

        self._build_cache(au_domain=self.au_domain, allowed_audience_fields=self.allowed_audience_fields)

    @classmethod
    def _build_cache(cls, allowed_audience_fields, au_domain=None):

        if au_domain is None or au_domain == '_global':
            au_domains = list(set(['_global', *cls.audience_domains]))
        else:
            au_domains = [au_domain]
        for d in au_domains:
            audience_queries, raw_data = cls.get_queries_from_db(au_domain=d,
                                                                 allowed_audience_fields=allowed_audience_fields)
            cls._queries_to_cache(au_domain=au_domain, audience_data=raw_data)

    @property
    def cache_audiences_key(self):

        return self._cache_audiences_key(au_domain=self.au_domain)

    @classmethod
    def _cache_audiences_key(cls, au_domain):

        return f'au:{cls.domain}:defs:{au_domain}'