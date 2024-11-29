import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/info/',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/logout/',
    method: 'post'
  })
}

export function CreateUser(data) {
  return request({
    url: '/users/create/',
    method: 'post',
    data
  })
}

export function DeleteUser(id) {
  return request({
    url: '/users/delete/' + id + '/',
    method: 'delete'
  })
}

export function ModifyUser(data, id) {
  return request({
    url: '/users/' + id + '/',
    method: 'put',
    data
  })
}

export function CreateShipCrew(data) {
  return request({
    url: '/shipcrew/create/',
    method: 'post',
    data
  })
}

export function SearchUser(text) {
  return request({
    url: '/users/?search=' + text,
    method: 'get'
  })
}
