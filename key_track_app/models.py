from django.db import models

class Personal(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name='Teléfono')
    code = models.CharField(max_length=255, unique=True, verbose_name='Código de barra')

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

    def __str__(self):
        return f"Entrega {self.id}"
    

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