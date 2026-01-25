from rest_framework import serializers
from fist_app.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = '__all__'
        fields = ['id', 'first_name', 'last_name', 'email', 'age', 'is_active']
        read_only_fields = ['id']

    def validate_email(self,value):
        """
        custom validation for email field
        """
        if self.instance:
            if self.instance.email != value:
                if Student.objects.filter(email=value).exists():
                    raise serializers.ValidationError("A student with this email already exist")
        else:
            if Student.objects.filter(email = value).exists():
                    raise serializers.ValidationError("A student with this email already exist")
        return value
    
    def validate_age(self,value):
         '''
         costom validation for age dield
         '''

         if value <6 or value > 130:
            raise serializers.ValidationError("age must be between 6 and 130")
         return value
              