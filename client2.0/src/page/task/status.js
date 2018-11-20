export const getColor = (item) => {
  switch (item.status) {
    case 'accept':
      return '#dfc052'
    case 'asign':
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
    case 'repair_audit':
      return '#ccc'
  }
}

export const getName = (item) => {
  switch (item.status) {
    case 'accept':
      return '待接报'
    case 'asign':
      return '待签到'
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
    case 'repair_audit':
      return '审核中'
  }
}
