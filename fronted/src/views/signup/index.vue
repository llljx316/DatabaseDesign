<template>
  <div>
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
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
    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogFormVisible = false; resetForm('ruleForm')">取 消</el-button>
      <el-button type="primary" @click="dialogFormVisible = false; submitForm('ruleForm')">确 定</el-button>
    </div>
  </div>
</template>
<script>
import { getShip } from '@/api/table'
import { CreateShipCrew, CreateUser, DeleteUser } from '@/api/user'

export default {
  name: 'SignUp',
  created() {
    this.shipsList()
  },
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

    return {
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
    ruleForm: {
      handler(newVal, oldVal) {
        // selectedType 变化时重新计算 visibleFields
        console.log('selectedType changed:', newVal)
      },
      immediate: true // 立即执行一次
    }
  },
  methods: {
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
    shipsList() {
      getShip().then(response => {
        this.shiplist = response.data.results
        // this.listLoading = false
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}

// export default {}
</script>
