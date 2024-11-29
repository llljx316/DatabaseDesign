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
      <el-table-column align="center" label="船ID" width="95">
        <template slot-scope="scope">
          {{ scope.row.shipid }}
        </template>
      </el-table-column>
      <el-table-column label="名称">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="类型" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ship_type }}</span>
        </template>
      </el-table-column>
      <el-table-column label="装载量" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.capacity }}
        </template>
      </el-table-column>
      <el-table-column label="长度" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.length }}
        </template>
      </el-table-column>
      <el-table-column label="宽度" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.width }}
        </template>
      </el-table-column>
      <el-table-column label="高度" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.height }}
        </template>
      </el-table-column>
      <el-table-column label="吃水" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.draft }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.status }}
        </template>
      </el-table-column>
      <el-table-column label="国家" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.country }}
        </template>
      </el-table-column>
      <el-table-column label="编辑" width="110" align="center">
        <!-- 存一下相应的id -->
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-edit" @click="nowid=scope.row.shipid; visible_edit=true" circle></el-button>

        </template>
      </el-table-column>
      <el-table-column label="删除" width="110" align="center">
        <template slot-scope="scope">
          <el-button type="danger" icon="el-icon-delete" @click="comformdelete(scope.row)" circle></el-button>
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
    <el-button  type="primary" icon="el-icon-plus" @click="visible_create=true" circle> </el-button>
    <el-dialog title="编辑" :visible.sync="visible_edit">
      <el-form :model="shipForm" status-icon ref="shipForm" label-width="100px" class="demo-shipForm">
        <el-form-item v-for="field in ship_visible" :key="field.key" :label="field.label" :prop="field.prop">
          <el-input v-if="field.type === 'text'" type="text" v-model="shipForm[field.prop]" autocomplete="off"></el-input>
          <el-input v-else type="number" v-model="shipForm[field.prop]" autocomplete="off"  step="0.01"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible_edit = false; resetForm('ruleForm')">取 消</el-button>
        <el-button type="primary" @click="visible_edit = false; ModifyShipFront('ruleForm')">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="创建" :visible.sync="visible_create">
      <el-form :model="shipForm" status-icon ref="shipForm" label-width="100px" class="demo-shipForm">
        <el-form-item v-for="field in ship_visible" :key="field.key" :label="field.label" :prop="field.prop">
          <el-input v-if="field.type === 'text'" type="text" v-model="shipForm[field.prop]" autocomplete="off"></el-input>
          <el-input v-else type="number" v-model="shipForm[field.prop]" autocomplete="off"  step="0.01"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible_edit = false; resetForm('ruleForm')">取 消</el-button>
        <el-button type="primary" @click="visible_edit = false; CreateShipFront('ruleForm')">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getShip, DeleteShip } from '@/api/table'
import { ModifyShip, CreateShip, SearchShip } from '@/api/ship';

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
      visible_edit: false,
      visible_create: false,
      searchText: '',
      shipForm: {
        name: '',
        ship_type: '',
        capacity: '',
        length: '',
        width: '',
        height: '',
        draft: '',
        status: '',
        country: ''
      },
      ship_visible: [
        { key: 'name', label: '船只名称', prop: 'name', type: 'text' },
        { key: 'ship_type', label: '船只类型', prop: 'ship_type', type: 'text' },
        { key: 'capacity', label: '载重量', prop: 'capacity', type: 'number' },
        { key: 'length', label: '船只长度', prop: 'length', type: 'number' },
        { key: 'width', label: '船只宽度', prop: 'width', type: 'number' },
        { key: 'height', label: '船只高度', prop: 'height', type: 'number' },
        { key: 'draft', label: '船只吃水', prop: 'draft', type: 'number' },
        { key: 'status', label: '船只状态', prop: 'status', type: 'text' },
        { key: 'country', label: '船只所属国家', prop: 'country', type: 'text' }
      ],
      nowid: ''
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
      getShip().then(response => {
        this.list = response.data.results
        this.listLoading = false
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    comformdelete(data) {
      this.$confirm('此操作将永久删除船只信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // console.log(this.list[1].shipid)
        const del_id = data.shipid
        DeleteShip(del_id).then(response => {
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
    ModifyShipFront(formName) {
      const id = this.nowid
      ModifyShip(this.shipForm, id).then(res => {
        console.log(res)
        // res1 = res
        if (res.status === 200) {
          // 判断是否创建其他的类型
          // console.log(this.shipForm.typevalue)
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
    CreateShipFront(formName) {
      CreateShip(this.shipForm).then(res => {
        console.log(res)
        // res1 = res
        if (res.status === 201) {
          // 判断是否创建其他的类型
          // console.log(this.shipForm.typevalue)
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
      SearchShip(this.searchText).then(res => {
        console.log(res)
        this.list = res.data.results
      })
    }
  }
}
</script>
