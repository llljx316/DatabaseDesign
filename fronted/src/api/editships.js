import request from '@/utils/request'

export function GetEditShips() {
  return request({
    url: '/editships/',
    method: 'get'
  })
}

export function SearchEditShips(attr, text) {
  console.log(text)
  return request({
    url: '/editships/?'+attr+'='+text,
    method: 'get'
  })
}
