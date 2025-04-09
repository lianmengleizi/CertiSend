from django.db import models

class UserInformation(models.Model):
    name = models.CharField('姓名', max_length=100)
    phone = models.CharField('电话', max_length=20)
    province = models.CharField('省份', max_length=50)  # 确保长度足够
    city = models.CharField('城市', max_length=50)  # 确保长度足够
    district = models.CharField('区县', max_length=50)  # 确保长度足够
    street = models.TextField('街道门牌号')
    exam_number = models.CharField('准考证号', max_length=50)
    id_number = models.CharField('身份证号', max_length=50)
    is_sent = models.BooleanField('是否发送', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    @property
    def full_address(self):
        return f"{self.district}{self.street}"

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
