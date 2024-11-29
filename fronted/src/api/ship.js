import request from '@/utils/request'

export function CreateShip(data) {
  return request({
    url: '/ships/author/',
    method: 'post',
    data
  })
}

// export function DeleteUser(id) {
//   return request({
//     url: '/users/delete/' + id + '/',
//     method: 'delete'
//   })
// }

export function ModifyShip(data, id) {
  return request({
    url: '/ships/author/' + id + '/',
    method: 'put',
    data
  })
}

export function SearchShip(text) {
  console.log(text)
  return request({
    url: '/ships/author/?search=' + text,
    method: 'get'
  })
}
