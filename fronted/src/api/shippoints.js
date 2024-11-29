import request from '@/utils/request'

export function CreateShipPoint(data) {
  return request({
    url: '/shippoints/',
    method: 'post',
    data
  })
}

export function getShipPoints(data) {
  return request({
    url: '/shippoints/',
    method: 'get'
  })
}

export function getShipRoutes(data) {
  return request({
    url: '/shiproutes/',
    method: 'get'
  })
}

export function getShipPointsEnd() {
  return request({
    url: '/shiproutes/end/',
    method: 'get'
  })
}

export function getShipPointsEndSearch(id) {
  return request({
    url: '/shiproutes/end/?id=' + id,
    method: 'get'
  })
}

// export function DeleteUser(id) {
//   return request({
//     url: '/users/delete/' + id + '/',
//     method: 'delete'
//   })
// }

export function ModifyShipPoint(data, id) {
  return request({
    url: '/shippoints/' + id + '/',
    method: 'put',
    data
  })
}

export function DeleteShipPoint(id) {
  return request({
    url: '/shippoints/' + id + '/',
    method: 'delete'
  })
}

// export function SearchShip(text) {
//   console.log(text)
//   return request({
//     url: '/shippoints/?search=' + text,
//     method: 'get'
//   })
// }
