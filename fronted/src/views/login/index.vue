<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">

      <div class="title-container">
        <h3 class="title">登录</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="Username"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="Password"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>
      <el-row>
        <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:10px" @click.native.prevent="handleLogin">登录</el-button>
      </el-row>
      <el-row>
        <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:10px" @click="dialogFormVisible = true">注册</el-button>
      </el-row>

    </el-form>

    <el-dialog title="注册" :visible.sync="dialogFormVisible">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm" :style="{ color: 'black' }">
        <el-form-item label="用户类型" :label-width="formLabelWidth">
          <el-select v-model="ruleForm.typevalue" placeholder="请选择">
            <el-option
              v-for="item in TypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-for="field in visibleFields" :key="field.key" :label="field.label" :prop="field.prop">
          <el-input v-if="field.type === 'text'" type="text" v-model="ruleForm[field.prop]" autocomplete="off"></el-input>
          <el-input v-else-if="field.type === 'password'" type="password" v-model="ruleForm[field.prop]" autocomplete="off"></el-input>
          <el-select  v-else-if="field.type === 'ship'" v-model="ruleForm[field.prop]" placeholder="请选择">
            <el-option
              v-for="item in shiplist"
              :key="item.shipid"
              :label="item.name"
              :value="item.shipid">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <SignUp />
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false; resetForm('ruleForm')">取 消</el-button>
        <el-button type="primary" @click="dialogFormVisible = false; submitForm('ruleForm')">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { validUsername } from '@/utils/validate'
import { CreateShipCrew, CreateUser, DeleteUser } from '@/api/user'
import { getShip } from '@/api/table'
// import { SignUp } from '@/views/signup/index.vue'

export default {
  name: 'Login',
  // components: {
  //   SignUp
  // },
  data() {
    var validateEmail = (rule, value, callback) => {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (value === '') {
        callback(new Error('请输入邮箱地址'))
      } else if (!emailPattern.test(value)) {
        callback(new Error('请输入有效的邮箱地址'))
      } else {
        callback()
      }
    }

    var validatePass = (rule, value, callback) => {
      if (value === '' || value.length <= 8) {
        callback(new Error('请输入大于8位的密码'))
      } else {
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    // return {
    //   ruleForm: {
    //     password: '',
    //     checkPass: '',
    //     age: ''
    //   },
    //   rules: {
    //     password: [
    //       { validator: validatePass, trigger: 'blur' }
    //     ],
    //     checkPass: [
    //       { validator: validatePass2, trigger: 'blur' }
    //     ],
    //     age: [
    //       { validator: checkAge, trigger: 'blur' }
    //     ]
    //   }
    // }
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('Please enter the correct user name'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: 'admin',
        password: '111111'
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined,
      ruleForm: {
        username: 'aaaa243',
        email: 'aaaasdsd',
        password: 'asdfasdfa',
        checkPass: 'asdfasdfa',
        typevalue: '',
        ShipID: '',
        roles: ''
      },
      // shipcrewForm: {
      //   user: '',
      //   ShipID: ''
      // },
      rules: {
        username: [
          { required: true }
        ],
        email: [
          { required: true, validator: validateEmail, trigger: 'blur' }
        ],
        password: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ],
        checkPass: [
          { required: true, validator: validatePass2, trigger: 'blur' }
        ]
      },
      dialogFormVisible: false,
      TypeOptions: [{
        value: 1,
        label: '管理员'
      }, {
        value: 2,
        label: '船员'
      }, {
        value: 3,
        label: '数据分析师'
      }],
      shiplist: null,
      SelectShipID: null
    }
  },
  computed: {
    visibleFields() {
      if (this.ruleForm.typevalue === this.TypeOptions.find(item => item.label === '管理员').value) { //管理员
        // this.ruleForm = {
        //   username: '',
        //   email: '',
        //   password: '',
        //   checkPass: '',
        //   is_staff: false
        // }
        return [
          { key: 'username', label: '用户名', prop: 'username', type: 'text' },
          { key: 'email', label: '邮箱', prop: 'email', type: 'text' },
          { key: 'password', label: '密码', prop: 'password', type: 'password' },
          { key: 'checkPass', label: '确认密码', prop: 'checkPass', type: 'password' }
        ]
      } else if (this.ruleForm.typevalue === this.TypeOptions.find(item => item.label === '船员').value) {
        this.shipsList()
        // this.ruleForm = {
        //   username: '',
        //   email: '',
        //   password: '',
        //   checkPass: '',
        //   ship: '',
        //   is_staff: true
        // }
        return [
          { key: 'username', label: '用户名', prop: 'username', type: 'text' },
          { key: 'email', label: '邮箱', prop: 'email', type: 'text' },
          { key: 'password', label: '密码', prop: 'password', type: 'password' },
          { key: 'checkPass', label: '确认密码', prop: 'checkPass', type: 'password' },
          { key: 'ship', label: '船只', prop: 'ShipID', type: 'ship' }
        ]
      }
      return []
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    },
    ruleForm: {
      handler(newVal, oldVal) {
        // selectedType 变化时重新计算 visibleFields
        console.log('selectedType changed:', newVal)
      },
      immediate: true // 立即执行一次
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm).then(() => {
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // handleSignup() {
    //   this.$router.push({ path: '/signup' })
    // },

    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log(this.ruleForm)
          console.log(this.ruleForm.typevalue)
          // let res1
          // const sF = this.shipcrewForm
          // const tv = this.ruleForm.typevalue
          if (this.ruleForm.typevalue === this.TypeOptions.find(item => item.label === '管理员').value) {
            this.ruleForm.roles = 0
          } else {
            this.ruleForm.roles = 1
          }

          CreateUser(this.ruleForm).then(res => {
            console.log(res)
            // res1 = res
            if (res.status === 201) {
              // 判断是否创建其他的类型
              console.log(this.ruleForm.typevalue)
              // this.$message({
              //   message: '创建成功',
              //   type: 'success'
              // })
            } else {
              this.$message({
                message: '创建失败',
                type: 'error'
              })
              console.log('error submit!!')
              return false
            }
          }).catch(() => {
            this.$message({
              message: '创建失败',
              type: 'error'
            })
            console.log('error submit!!')
            return false
          })
          // }).then(() => {
          //   if (tv === this.TypeOptions.find(item => item.label === '船员').value) {
          //     console.log(sF)
          //     sF.user = res1.data.id
          //     CreateShipCrew(sF).then(res => {
          //       console.log(res)
          //       if (res.status === 201) {
          //         this.$message({
          //           message: '创建成功',
          //           type: 'success'
          //         })
          //       } else {
          //         this.$message({
          //           message: '创建失败',
          //           type: 'error'
          //         })
          //         // 回滚
          //         DeleteUser(res1.id)
          //         console.log('error submit!!')
          //         return false
          //       }
          //     })
          //   }
          //   // alert('submit!')
          // })
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    // 获取船只列表
    shipsList() {
      getShip().then(response => {
        this.shiplist = response.data.results
        // this.listLoading = false
      })
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  ::v-deep .el-select-dropdown__item.selected {
    color: black; /* 选中的字体颜色 */
  }
}
</style>
