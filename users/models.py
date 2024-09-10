from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):    

    def create_user(self, userID , email, phone_number, name, password=None, **extra_fields):

        if not email:            
            raise ValueError('이메일을 입력해야 합니다.')
        if not userID:
            raise ValueError('사용자 ID는 필수입니다.')
        if not phone_number:
            raise ValueError('전화번호는 필수입니다.')
        email = self.normalize_email(email)
        user = self.model(
            userID=userID, 
            email=email, 
            phone_number=phone_number, 
            name=name,
            **extra_fields
        )
        
        user.set_password(password)        
        user.save(using=self._db)        
        return user

    def create_superuser(self, userID, email, phone_number, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        #extra_fields.setdefault('is_admin', True)
        return self.create_user(userID, email, phone_number, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):    

    userID = models.CharField(max_length=20, primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=30)
    phone_number = models.IntegerField(unique=True, blank=False)
    address = models.TextField(max_length=100)
    make_date = models.DateField(auto_now_add=True)
    is_owner = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    #is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'userID'    
    REQUIRED_FIELDS = ['name', 'phone_number', 'email',]
    
    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
    
    def __str__(self):
        return self.userID

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    #@property
    #def is_staff(self):
        #return self.is_admin

