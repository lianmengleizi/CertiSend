import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // 改成你的后端地址和端口
  timeout: 5000,
})

instance.interceptors.response.use(
  res => res.data,
  err => {
    console.error(err)
    return Promise.reject(err)
  }
)
const getUserInfo = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/user-info/');
      console.log('用户信息:', response.data);
    } catch (error) {
      console.error('获取用户信息失败:', error);
    }
  };
  
  getUserInfo();
export default instance
