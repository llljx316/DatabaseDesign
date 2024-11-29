import request from '@/utils/request'

export function GetEditShipPoints() {
  return request({
    url: '/editshippoints/',
    method: 'get'
  })
}

export function SearchEditShipPoints(text) {
  console.log(text)
  return request({
    url: '/editshippoints/?search='+text,
    method: 'get'
  })
}
