<template>
  <div class="app-container">
    <el-input
      type="text"
      prefix-icon="el-icon-search"
      v-model="searchText"
      placeholder="请输入"
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
      <el-table-column align="center" label="时间" width="200">
        <template slot-scope="scope">
          {{ scope.row.time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="事件">
        <template slot-scope="scope">
          {{ scope.row.content }}
        </template>
      </el-table-column>
      <el-table-column label="发布者" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.user.username }}</span>
        </template>
      </el-table-column>
      <el-table-column label="发布者邮箱" width="150" align="center">
        <template slot-scope="scope">
          {{ scope.row.user.email }}
        </template>
      </el-table-column>

    </el-table>
    <el-button type="primary" icon="el-icon-plus" @click="visible_create=true"></el-button>
    <el-dialog title="创建" :visible.sync="visible_create">
      <el-form :model="eventForm" status-icon ref="eventForm" label-width="100px" class="demo-eventForm">
        <el-input type="text" v-model="eventForm['content']" autocomplete="off"></el-input>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible_edit = false; resetForm('ruleForm')">取 消</el-button>
        <el-button type="primary" @click="visible_edit = false; CreateShipFront('ruleForm')">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { GetEvents, CreateEvent, SearchEvent } from '@/api/event';

export default {
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
    return {
      list: null,
      listLoading: true,
      // visible_edit: false,
      visible_create: false,
      searchText: '',
      eventForm: {
        content: ''
      },
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    test(data) {
      console.log(data.row.shipid)
    },
    fetchData() {
      this.listLoading = true
      GetEvents().then(response => {
        this.list = response.data.results
        this.listLoading = false
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    // comformdelete(data) {
    //   this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
    //     confirmButtonText: '确定',
    //     cancelButtonText: '取消',
    //     type: 'warning'
    //   }).then(() => {
    //     // console.log(this.list[1].shipid)
    //     const del_id = data.shipid
    //     DeleteShip(del_id).then(response => {
    //       this.fetchData()
    //       this.$message({
    //         type: 'success',
    //         message: '删除成功!'
    //       })
    //     }).catch(() => {
    //       this.$message({
    //         type: 'warning',
    //         message: '删除失败!'
    //       })
    //     })
    //   }).catch(() => {
    //     this.$message({
    //       type: 'info',
    //       message: '已取消删除'
    //     })
    //   })
    // },
    // ModifyShipFront(formName) {
    //   const id = this.nowid
    //   ModifyShip(this.eventForm, id).then(res => {
    //     console.log(res)
    //     // res1 = res
    //     if (res.status === 200) {
    //       // 判断是否创建其他的类型
    //       // console.log(this.eventForm.typevalue)
    //       this.fetchData()
    //       // this.$message({
    //       //   message: '创建成功',
    //       //   type: 'success'
    //       // })
    //     } else {
    //       this.$message({
    //         message: '创建失败',
    //         type: 'error'
    //       })
    //       console.log('error submit!!')
    //       return false
    //     }
    //   }).catch(() => {
    //     this.$message({
    //       message: '创建失败',
    //       type: 'error'
    //     })
    //     console.log('error submit!!')
    //     return false
    //   })
    // },
    CreateShipFront(formName) {
      CreateEvent(this.eventForm).then(res => {
        console.log(res)
        // res1 = res
        if (res.status === 201) {
          // 判断是否创建其他的类型
          // console.log(this.eventForm.typevalue)
          this.fetchData()

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
    },
    handleSearch() {
      SearchEvent(this.searchText).then(res => {
        console.log(res)
        this.list = res.data.results
      })
    }
  }
}
</script>
