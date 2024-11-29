import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}

export function getShip(params) {
  return request({
    url: '/ships/',
    method: 'get',
    params
  })
}

export function DeleteShip(id) {
  return request({
    url: '/ships/author/' + id + '/',
    method: 'delete'
  })
}
