import graphene
from graphene_django import DjangoObjectType

from formapp.models import FormData

class FormDataType(DjangoObjectType):
    class Meta:
        model = FormData
        fields = ("id", "name", "fee", "rate", "covlim", "minprem")

class Query(graphene.ObjectType):
    formdata_by_name = graphene.Field(FormDataType, name=graphene.String(required=True))

    def resolve_formdata_by_name(root, info, name):
        try:
            return FormData.objects.get(name=name)
        except FormData.DoesNotExist:
            return None
        
class FormDataMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        fee = graphene.Decimal(required=True)
        rate = graphene.Decimal(required=True)
        covlim = graphene.Decimal(required=True)
        minprem = graphene.Decimal(required=False)

    form_data = graphene.Field(FormDataType)

    @classmethod
    def mutate(cls, root, info, name, fee, rate, covlim, minprem=None):
        form_data = FormData(
            name=name,
            fee=fee,
            rate=rate,
            covlim=covlim,
            minprem=minprem
        )
        form_data.save()
        return FormDataMutation(form_data=form_data)

class UpdateFormDataMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        fee = graphene.Decimal(required=True)
        rate = graphene.Decimal(required=True)
        covlim = graphene.Decimal(required=True)
        minprem = graphene.Decimal(required=False)

    form_data = graphene.Field(FormDataType)

    @classmethod
    def mutate(cls, root, info, name, fee, rate, covlim, minprem=None):
        try:
            form_data = FormData.objects.get(name=name)
            form_data.fee = fee
            form_data.rate = rate
            form_data.covlim = covlim
            form_data.minprem = minprem
            form_data.save()
            return UpdateFormDataMutation(form_data=form_data)
        except FormData.DoesNotExist:
                return None

class Mutation(graphene.ObjectType):
    add_form_data = FormDataMutation.Field()
    update_form_data = UpdateFormDataMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)