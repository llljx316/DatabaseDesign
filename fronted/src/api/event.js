import request from '@/utils/request'

export function GetEvents() {
  return request({
    url: '/events/',
    method: 'get'
  })
}

export function CreateEvent(data) {
  return request({
    url: '/events/create/',
    method: 'post',
    data
  })
}

export function SearchEvent(text) {
  return request({
    url: '/events/?search='+text,
    method: 'get'
  })
}
