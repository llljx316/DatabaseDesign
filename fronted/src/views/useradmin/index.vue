<template>
  <div class="app-container">
    <el-input
      type="text"
      prefix-icon="el-icon-search"
      v-model="searchText"
      placeholder="请输入用户名或邮箱查找"
      style="width: 270px; cursor: pointer"
      @enter="handleSearch"
    ></el-input>
    <el-button type="primary" icon="el-icon-search" @click="handleSearch">
    </el-button>
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="用户名">
        <template slot-scope="scope">
          {{ scope.row.username }}
        </template>
      </el-table-column>
      <el-table-column label="邮箱" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.email }}</span>
        </template>
      </el-table-column>
      <el-table-column label="身份" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.roles }}
        </template>
      </el-table-column>
      <el-table-column label="类型" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.typevalue }}
        </template>
      </el-table-column>
      <el-table-column label="编辑" v-if=visibleDeleteEdit width="110" align="center">
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-edit" @click="edit(scope.row)" circle></el-button>
        </template>
      </el-table-column>
      <el-table-column label="删除" v-if=visibleDeleteEdit width="110" align="center">
        <template slot-scope="scope">
          <el-button type="danger" icon="el-icon-delete" @click=comformdelete(scope.row) circle></el-button>
        </template>
      </el-table-column>
      <!-- <el-table-column class-name="status-col" label="Status" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="Display_time" width="200">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.display_time }}</span>
        </template>
      </el-table-column> -->
    </el-table>
    <!-- <el-button type="primary" icon="el-icon-search" title="添加用户" @click='visible_add_user=true' ></el-button>
    <SignUp
      :ruleForm="ruleFormSign"
      :rules="rules"
      :dialogFormVisible="visible_add_user"
      :TypeOptions="TypeOptions"
      :shiplist="shiplist"
      :SelectShipID="SelectShipID"></SignUp> -->
    <el-dialog title="编辑" :visible.sync="dialogFormVisible">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
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
    </el-dialog>

  </div>
</template>

<script>
import { getList, getShip } from '@/api/table'
import { DeleteUser, ModifyUser, SearchUser } from '@/api/user'
import { SignUp } from '@/views/signup/index.vue'
import { Footer } from '@/views/signup/Footer.vue'


export default {
  components: {
    SignUp,Footer
  },
  created() {
    this.fetchData()
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
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
      list: null,
      listLoading: true,
      ruleForm: {
        username: '',
        email: '',
        password: '',
        checkPass: '',
        typevalue: '',
        ShipID: '',
        roles: ''
      },
      shiplist: null,
      dialogFormVisible: false,
      editid: '',
      searchText: '',
      ruleFormSign: {
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
      visible_add_user: true,
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
      // shiplist: null,
      SelectShipID: null,
      visibleDeleteEdit: this.$store.state.user.typevalue === 1
    }
  },
  computed: {
    visibleFields() {
      if (this.ruleForm.typevalue === 1) { // 管理员
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
      } else if (this.ruleForm.typevalue === 2) {
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
    fetchData() {
      this.listLoading = true
      getList().then(response => {
        this.list = response.data.results
        console.log(this.list)
        // this.list.roles = this.list.roles==0?'管理员':'用户'
        // this.list.typevalue = this.list.typevalue==0?'管理员':this.list.typevalue==1?'船员':'数据分析师'
        this.listLoading = false
      })
    },
    comformdelete(row) {
      this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log(this.list[1].id)
        const del_id = row.id
        DeleteUser(del_id).then(response => {
          this.fetchData()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        }).catch(() => {
          this.$message({
            type: 'warning',
            message: '删除失败!'
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    edit(data) {
      this.dialogFormVisible = true

      this.ruleForm.typevalue = data.typevalue
      this.ruleForm.username = data.username
      this.ruleForm.email = data.email
      this.ruleForm.shipid = data.shipid

      this.editid = data.id
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log(this.ruleForm)
          console.log(this.ruleForm.typevalue)
          // let res1
          // const sF = this.shipcrewForm
          // const tv = this.ruleForm.typevalue
          if (this.ruleForm.typevalue === 1) {
            this.ruleForm.roles = 0
          } else {
            this.ruleForm.roles = 1
          }
          const id = this.editid
          ModifyUser(this.ruleForm, id).then(res => {
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
    handleSearch() {
      SearchUser(this.searchText).then(res => {
        console.log(res)
        this.list = res.data.results
      })
    }
  }
}

</script>
