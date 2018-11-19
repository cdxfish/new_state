export const getColor = (item) => {
  switch (item.status) {
    case 'accept':
      return '#dfc052'
    case 'unfinished':
      return '#2583cf'
    case 'repair':
      return '#366092'
    case 'finish':
      return '#94bb47'
    case 'audit':
      return '#d74a88'
    case 'exchange_out':
      return '#40b9e1'
    case 'turn':
      return '#fd7488'
    case 'suspended':
      return '#999'
    case 'unuse':
      return '#ccc'
  }
}

export const getName = (item) => {
  switch (item.status) {
    case 'accept':
      return '待接报'
    case 'unfinished':
      return '待执行'
    case 'repair':
      return '维修中'
    case 'finish':
      return '已完成'
    case 'audit':
      return '销项中'
    case 'exchange_out':
      return '转发中'
    case 'turn':
      return '交接中'
    case 'suspended':
      return '已挂起'
    case 'unuse':
      return '无效工单'
  }
}
