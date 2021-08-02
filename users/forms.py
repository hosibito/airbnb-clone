from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        # print(self.cleaned_data)  # {'email': 'lalalalal', 'password': 'argare'}
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                # raise forms.ValidationError("Password is wrong")
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            # raise forms.ValidationError("User does not exist")
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(UserCreationForm):
    class Meta:
        model = models.User  # 모델지정
        fields = ("username", "first_name", "last_name")

    username = forms.EmailField(label="Email")


"""

class SignUpForm(forms.ModelForm):  # 모델폼 이용
    class Meta:
        model = models.User  # 모델지정
        fields = ("first_name", "last_name", "email")
        # 입력 필드 지정(admin 참조)
        # 없는건 디폴트값이 있어야함. (아님 Required 값에서 오류남. )

    password = forms.CharField(widget=forms.PasswordInput)  # 패스워드 확인은 모델에 없으므로...
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):   # 순차적 처리
        password = self.cleaned_data.get("password")  # 순차적처리를 햇으므로 password 를 가져올수 있다.
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # 유저명을 Email 로 하고 싶으므로.. (유저명을 그대로 사용한다면 할 필요 없슴..)
    def save(self, *args, **kwargs):  # ModelForm 에는 이미 존재한다. 오버라이딩한다.

        user = super().save(commit=False)
        # commit=False 생성은 하되 아직 DB에 commit 하지 않은 상태로 있는다.

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email   # 이렇게 옵션을 추가하기 위해 commit 하지 않은 상태의 데이터가 필요!
        user.set_password(password)  # 암호화된 페스워드를 준다.
        user.save()
"""

"""
ModelForm 을 이용하지 않았을때.. #15 SIGN UP 클래스 형으로 구현.(기본 흐름. ) 참조

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):   # 순차적 처리
        password = self.cleaned_data.get("password")  # 순차적처리를 햇으므로 password 를 가져올수 있다.
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self):  # 이걸.. forms에 둘지 views에 둘지는 고민해야할 문제임.
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # models.User.objects.create()  보통은 이걸 사용해야 하나. 유저는 password를 암호화해야한다.
        user = models.User.objects.create_user(email, email, password)
        # 장고 usermodel에서 제공.. username,email,password 순이나 유저네임을 이메일로 이용할것이므로...
        user.first_name = first_name
        user.last_name = last_name
        user.save()
"""
"""
    # #4 USER LOG IN & LOG OUT - 도움없이 구현 cleaned_data 개념정리 확인인할것
    def clean_email(self):
        # print("clean email")
        print(self.cleaned_data)  # {'email': 'test@test.com'}
        return "lalalalal"

    def clean_password(self):
        # print("clean password")
        print(self.cleaned_data)  # {'email': 'lalalalal', 'password': 'argare'}
        return "lalalalal"



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 각항목이름 앞 clean_ 으로 접근
    # 정리된 데이터 결과값에 접근하는것임
    def clean_email(self):
        # print("clean email")
        print(self.cleaned_data)  # {'email': 'test@test.com'}
        email = self.cleaned_data.get("email")

        try:
            models.User.objects.get(username=email)  # 니콜라스는 유저이름을 이메일로 하는걸 선호함
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        # print("clean password")
        print(self.cleaned_data)  # {'email': 'lalalalal', 'password': 'argare'}
        return "lalalalal"

이메일과 페스워드 두군데의 처리를 했으나..
깔끔하지 않고 반복된다.
서로 관련있는 것은 하나로 묶을수 있다.
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 각항목이름 앞 clean_ 으로 접근
    # 정리된 데이터 결과값에 접근하는것임
    def clean_email(self):
        # print(self.cleaned_data)  # {'email': 'test@test.com'}
        email = self.cleaned_data.get("email")

        try:
            models.User.objects.get(username=email)  # 니콜라스는 유저이름을 이메일로 하는걸 선호함
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        # print(self.cleaned_data)  # {'email': 'lalalalal', 'password': 'argare'}
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return password
            else:
                raise forms.ValidationError("Password is wrong")
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")
"""
