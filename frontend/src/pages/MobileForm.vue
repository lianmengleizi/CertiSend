<template>
  <div class="form-container">
    <div class="header">
      <img src="@/assets/admin-avatar.jpg" class="avatar" />
      <h2>信息填写</h2>
      <p class="tip">请认真填写，信息错误将无法收到证书</p>
    </div>

    <van-form @submit="onSubmit" class="form-box">
      <van-cell-group inset>
        <van-field
          v-model="form.name"
          label="姓名"
          placeholder="请输入真实姓名"
          :rules="[{ required: true, message: '请填写姓名' }]"
        />

        <van-field
          v-model="form.phone"
          type="tel"
          label="手机号"
          placeholder="请输入手机号"
          :rules="[{ validator: validatePhone, message: '请输入正确手机号' }]"
        />

        <van-field
          readonly
          clickable
          name="area"
          v-model="form.regionText"
          label="省市区"
          placeholder="点击选择省市区"
          @click="showArea = true"
          :rules="[{ required: true, message: '请选择省市区' }]"
        >
          <template #right-icon>
            <van-icon v-if="form.regionText" name="success" color="#07c160" />
          </template>
        </van-field>

        <van-popup v-model:show="showArea" position="bottom" round>
          <van-area
            :area-list="areaList"
            @confirm="onAreaConfirm"
            @cancel="showArea = false"
          />
        </van-popup>

        <van-field
          v-model="form.address"
          type="textarea"
          rows="1"
          autosize
          label="详细地址"
          placeholder="街道门牌号等详细地址"
          :rules="[{ required: true, message: '请填写详细地址' }]"
        />

        <van-field
          v-model="form.examNumber"
          label="准考证号"
          placeholder="请输入准考证号"
          :rules="[{ required: true, message: '请填写准考证号' }]"
        />

        <van-field
          v-model="form.idNumber"
          label="身份证号"
          placeholder="请输入身份证号"
          :rules="[{ validator: validateID, message: '请输入正确身份证号' }]"
        />
      </van-cell-group>

      <div class="submit-btn">
        <van-button
          round
          block
          type="primary"
          native-type="submit"
          :loading="submitting"
        >
          提交信息
        </van-button>
      </div>
    </van-form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { showSuccessToast, showToast } from "vant";
import { areaList } from "@vant/area-data";
import axios from "axios";

const showArea = ref(false);
const submitting = ref(false);
const form = ref({
  name: "",
  phone: "",
  address: "",
  examNumber: "",
  idNumber: "",
  regionText: "",
  province: "",
  city: "",
  county: "",
});

const onAreaConfirm = (result) => {
  showArea.value = false;

  if (!result || !result.selectedOptions) {
    console.error("地址选择返回值格式错误:", result);
    return;
  }

  const selectedOptions = result.selectedOptions;
  console.log(result, "result");

  form.value.regionText = selectedOptions
    .filter((item) => !!item)
    .map((item) => item.text)
    .join(" ");

  form.value.province = selectedOptions[0]?.value || "";
  form.value.city = selectedOptions[1]?.value || "";
  form.value.county = selectedOptions[2]?.value || "";
  console.log(form.value);
};

const validatePhone = (val) => /^1[3-9]\d{9}$/.test(val);
const validateID = (val) =>
  /^[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/.test(
    val
  );

const onSubmit = async () => {
  if (!form.value.regionText) {
    showToast("请选择省市区");
    return;
  }

  if (!form.value.address) {
    showToast("请输入详细地址");
    return;
  }

  submitting.value = true;

  try {
    const fullAddress = `${form.value.province}${form.value.city}${form.value.county}${form.value.address}`;

    const submitData = {
      name: form.value.name,
      phone: form.value.phone,
      province: form.value.province,
      city: form.value.city,
      district: form.value.county, // 修改为 `district`
      street: form.value.address, // 确保传递了 address（对应后台的 street）
      full_address: fullAddress,
      exam_number: form.value.examNumber,
      id_number: form.value.idNumber,
    };

    console.log("提交数据:", submitData);

    const response = await axios.post(
      "http://127.0.0.1:8000/api/user-info/",
      submitData
    );

    showSuccessToast("提交成功");

    // 提交成功后可以重置表单
    // resetForm();
    resetForm();
  } catch (error) {
    console.error("提交失败:", error);
    showToast("提交失败，请重试");
  } finally {
    submitting.value = false;
  }
};

// 可选：重置表单方法
const resetForm = () => {
  form.value = {
    name: "",
    phone: "",
    address: "",
    examNumber: "",
    idNumber: "",
    regionText: "",
    province: "",
    city: "",
    county: "",
  };
};
</script>

<style scoped>
.form-container {
  padding: 20px;
  background: linear-gradient(to bottom, #f5f7fa, #e4e8eb);
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 10px;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
  margin-bottom: 5px;
}

.tip {
  color: #666;
  font-size: 14px;
}

.form-box {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.submit-btn {
  margin: 20px 16px;
}

/* 地址选择字段样式 */
.van-field__control--right {
  color: #07c160;
}
</style>