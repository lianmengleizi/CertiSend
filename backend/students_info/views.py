from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from china_division import get_division_info
from rest_framework import viewsets
from .models import UserInformation
from .serializers import UserInformationSerializer


def get_region_from_code(area_code):
    print('area_code', area_code)
    if not area_code or not isinstance(area_code, str) or not area_code.isdigit():
        print(f"无效的地区编码格式: {area_code}")
        return "未知地区"

    division_info = get_division_info(area_code)
    print(f"地区编码: {area_code}, 返回信息: {division_info}")
    return division_info



class UserInformationAPIView(APIView):
    def get(self, request):
        user_info = UserInformation.objects.all()
        serializer = UserInformationSerializer(user_info, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        if not data.get('street'):
            return Response({"error": "详细地址不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        # 打印原始编码以便调试
        print(f"原始编码 - 省: {data.get('province')}, 市: {data.get('city')}, 区: {data.get('district')}")

        province_name = get_region_from_code(data.get('province', ''))
        city_name = get_region_from_code(data.get('city', ''))
        district_name = get_region_from_code(data.get('district', ''))

        # 创建用户信息
        user_info = UserInformation(
            name=data.get('name'),
            phone=data.get('phone'),
            province=province_name,
            city=city_name,
            district=district_name,
            street=data.get('street'),
            exam_number=data.get('exam_number'),
            id_number=data.get('id_number')
        )

        user_info.save()

        return Response(
            {'message': '提交成功', 'user': UserInformationSerializer(user_info).data},
            status=status.HTTP_201_CREATED
        )

class UserInformationViewSet(viewsets.ModelViewSet):
    queryset = UserInformation.objects.all()
    serializer_class = UserInformationSerializer

    def update(self, request, *args, **kwargs):
        # 获取要更新的记录
        instance = self.get_object()
        # 使用序列化器更新数据
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # partial=True 只更新提供的字段
        if serializer.is_valid():
            serializer.save()  # 保存更新后的记录
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)