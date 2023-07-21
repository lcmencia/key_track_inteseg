from django.db import models
from django.forms import ValidationError
from django.core.validators import RegexValidator

class Personal(models.Model):
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    documentNumberRegex = RegexValidator(regex = r"^[\d.-]+$")
    name = models.CharField(max_length=255, verbose_name='Nombre')
    email = models.EmailField()
    phone = models.CharField(validators = [phoneNumberRegex], max_length = 16, verbose_name='Teléfono')
    code = models.CharField(max_length=255, unique=True, verbose_name='Código de barra')
    document_number = models.CharField(validators = [documentNumberRegex], max_length=255, verbose_name='Cédula')

    class Meta:
        verbose_name_plural = "Personales"

    def __str__(self):
        return self.name
    
class Key(models.Model):
    number = models.CharField(max_length=255, verbose_name='Numero')
    code = models.CharField(max_length=255, unique=True, verbose_name='Código de barra')

    class Meta:
        verbose_name = "Llave"
        verbose_name_plural = "Llaves"

    def __str__(self):
        return self.number

class KeyHandover(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('entregado', 'Entregado'),
    ]
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, verbose_name='Personal')
    personal_code = models.CharField(max_length=255, verbose_name='Código de barra del Personal', blank=True, null=True)
    key = models.ForeignKey(Key, on_delete=models.CASCADE, verbose_name='Llave')
    key_code = models.CharField(max_length=255, verbose_name='Código de barra de la Llave', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente', verbose_name='Estado')
    class Meta:
        verbose_name = "Entrega de Llave"
        verbose_name_plural = "Entregas"
        constraints = [
            models.UniqueConstraint(
                fields=['personal', 'key'],
                condition=models.Q(status='pendiente'),
                name='unique_pending_key_handover'
            )
        ]

    def __str__(self):
        return f"Entrega {self.id}"

    def clean(self):
        # Comprobar si ya existe una entrega pendiente con la misma combinación de personal y key
        if not Personal.objects.filter(code=self.personal_code).exists():
            raise ValidationError({
                'personal_code': 'Este código no corresponde a ningun personal.'
            })
        
        if not Key.objects.filter(code=self.key_code).exists():
            raise ValidationError({
                'key_code': 'Este código no corresponde a ninguna Llave.'
            })
        
        key = Key.objects.get(code=self.key_code)
        if self.status == 'pendiente' and KeyHandover.objects.filter(key=key, status='pendiente').exists():
            raise ValidationError('Ya existe una entrega pendiente para este personal y llave.')
    

class KeyReception(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, verbose_name='Personal')
    key = models.ForeignKey(Key, on_delete=models.CASCADE, verbose_name='Llave')
    key_code = models.CharField(max_length=255, verbose_name='Código de barra de la Llave', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recepción de Llave"
        verbose_name_plural = "Recepción"

    def __str__(self):
        return f"Recepción {self.id}"
    
    def clean(self):

        if not Key.objects.filter(code=self.key_code).exists():
            raise ValidationError({
                'key_code': 'Este código no corresponde a ninguna Llave.'
            })
        
        key = Key.objects.get(code=self.key_code)
        
        if not KeyHandover.objects.filter(key=key, status='pendiente').exists():
            raise ValidationError('Esta llave ya ha sido devuelta.')
        

        