from rest_framework import serializers
from .models import Doctor, Patient, Appointment
from django.utils import timezone
from datetime import datetime 

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "phone_number",
            "email"
        ]

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "phone_number",
            "email",
            "address"
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient', write_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), source='doctor', write_only=True)
    class Meta:
        model = Appointment
        fields = [
            'id',
            'doctor',
            'doctor_id',
            'patient',
            'patient_id',
            'date',
            'at_time',
            'details'
        ]

    def Appointment(self, validated_data):
        return Appointment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.doctor = validated_data.get('doctor', instance.doctor)
        instance.patient = validated_data.get('patient', instance.patient)
        instance.date = validated_data.get('date', instance.date)
        instance.at_time = validated_data.get('at_time', instance.at_time)
        instance.details = validated_data.get('details', instance.details)
        instance.save()
        return instance
    
    def validate(self, data):
        if data['date'] < timezone.now().date() or data['at_time'] < timezone.now().time():
            raise serializers.ValidationError("The appointment date or time must be in the future.")
        return data