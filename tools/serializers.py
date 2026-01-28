from rest_framework import serializers
# from django.utils.datastructures import  MultiValueDict


class ModelSerializerId(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if data:
            if isinstance(data,int):
                return self.Meta.model.objects.get(id=data)
            elif isinstance(data,str):
                try:
                    return self.Meta.model.objects.get(id=int(data))
                except:
                    pass
          #  elif isinstance(data,MultiValueDict):
          #      ls = [ int(v) for k,v in data.items() ]
          #      return self.Meta.model.objects.filter(id__in=ls)
            else:
                return self.Meta.model.objects.get(id=int(data['id']))
        return None