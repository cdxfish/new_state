export const getColor = (item) => {
  switch (item) {
    case 'admissible':
      return '#dfc052'
    case 'under_repair':
      return '#2583cf'
    case 'wait_carry':
      return '#9981c6'
    case 'notify':
      return '#366092'
    case 'output_complete':
      return '#94bb47'
    case 'processed':
      return '#d74a88'
    case 'reject':
      return '#40b9e1'
    case 'deal_complete':
      return '#0081c6'
  }
}

export const getName = (item) => {
  switch (item) {
    case 'admissible':
      return '待受理'
    case 'under_repair':
      return '维修中'
    case 'notify':
      return '已指派'
    case 'deal_complete':
      return '已完成'
    case 'output_complete':
      return '已销项'
    case 'processed':
      return '已处理'
    case 'reject':
      return '已拒绝'
    case 'wait_carry':
      return '待提报'
  }
}
export const getUrgency = (item) => {
  switch (item) {
    case 'urgent':
      return '需加急处理'
    case 'normal':
      return '正常处理'
  }
}
export const getClssify = (item) => {
  switch (item) {
    case 'driving':
      return '影响行车'
    case 'passenger_flow':
      return '影响客运'
  }
}
export const getReback = (item) => {
  switch (item) {
    case 'processed':
      return '已处理'
    case 'untreated':
      return '未处理'
  }
}
export const getLable = (item) => {
  switch (item) {
    case 'pm':
      return '预防性维修'
    case 'cm':
      return '故障性维修'
    case false :
      return '无'
  }
}
export const getAssess = (item) => {
  switch (item) {
    case 'very_nice':
      return '非常好'
    case 'fine':
      return '很好'
    case 'commonly':
      return '一般'
    case 'difference':
      return '差'
    case 'very_poor':
      return '非常差'
  }
}
