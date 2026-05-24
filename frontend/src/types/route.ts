/**
 * 颜色旅行路径系统类型定义
 *
 * 接口说明（供离线 demo 兜底用）：
 *   parseRouteInput(input)  → ColorRouteSuggestion[]
 *   输入抖音链接或文字，在联网规划失败时返回一组本地路线建议
 */

/** 路径上的一个颜色点位 */
export interface ColorRoutePoint {
  /** 点位名称 */
  name: string
  /** 坐标 */
  location: { lat: number; lng: number }
  /** 关联色值 */
  color: string
  /** 颜色名称（如"朱红""琥珀"） */
  colorName: string
  /** 点位描述 */
  description: string
  /** 排序权重 */
  order: number
}

/** 整条颜色旅行路线 */
export interface ColorRouteSuggestion {
  /** 路线标题 */
  title: string
  /** 路线描述 */
  description: string
  /** 路线主题色（取主色） */
  themeColor: string
  /** 途径点位 */
  points: ColorRoutePoint[]
}

/** 输入来源类型 */
export type RouteInputSource = 'douyin' | 'text'

/** 输入解析结果 */
export interface RouteParseResult {
  source: RouteInputSource
  rawInput: string
  /** 联网规划失败时的备用建议路线 */
  suggestions: ColorRouteSuggestion[]
}

/**
 * 解析用户输入，返回颜色路线建议
 *
 * 备用数据：按关键词返回紫金港周边预设路线。
 */
export function parseRouteInput(input: string): ColorRouteSuggestion[] {
  const kw = input.toLowerCase()

  // 红色系路线
  if (kw.includes('红') || kw.includes('red') || kw.includes('热烈')) {
    return [{
      title: '红色·紫金印象',
      description: '从西溪到紫金港，寻一抹红色',
      themeColor: '#FF0000',
      points: [
        { name: '紫金港·南大门', location: { lat: 30.3005, lng: 120.0850 }, color: '#CC0000', colorName: '正红', description: '南大门的红色拱门', order: 1 },
        { name: '西溪·梅林', location: { lat: 30.2720, lng: 120.0580 }, color: '#E34234', colorName: '朱红', description: '冬日盛开的红色梅花', order: 2 },
        { name: '西溪天堂·湿地博物馆', location: { lat: 30.2690, lng: 120.0650 }, color: '#CB4154', colorName: '砖红', description: '博物馆的红砖外墙', order: 3 },
        { name: '三墩老街·夕照', location: { lat: 30.3180, lng: 120.0680 }, color: '#800020', colorName: '酒红', description: '老街黄昏的酒红色余晖', order: 4 },
      ],
    }]
  }

  // 蓝色系路线
  if (kw.includes('蓝') || kw.includes('blue') || kw.includes('清新')) {
    return [{
      title: '蓝色·启真水色',
      description: '紫金港周边的蓝色水系',
      themeColor: '#4B9FE3',
      points: [
        { name: '紫金港·启真湖', location: { lat: 30.3042, lng: 120.0826 }, color: '#87CEEB', colorName: '天蓝', description: '启真湖倒映的蓝天', order: 1 },
        { name: '西溪·湿地湖泊', location: { lat: 30.2705, lng: 120.0590 }, color: '#30D5C8', colorName: '湖蓝', description: '湿地湖面的清透蓝色', order: 2 },
        { name: '余杭塘河', location: { lat: 30.3090, lng: 120.0790 }, color: '#4B0082', colorName: '靛蓝', description: '河水的靛蓝色调', order: 3 },
        { name: '紫金港·蓝桥', location: { lat: 30.3055, lng: 120.0835 }, color: '#0047AB', colorName: '钴蓝', description: '校园蓝桥的钴蓝栏杆', order: 4 },
      ],
    }]
  }

  // 黄色/金色系路线
  if (kw.includes('黄') || kw.includes('金') || kw.includes('yellow') || kw.includes('温暖')) {
    return [{
      title: '金色·西溪秋韵',
      description: '紫金港周边的金色光影',
      themeColor: '#FFD700',
      points: [
        { name: '紫金港·银杏大道', location: { lat: 30.3030, lng: 120.0840 }, color: '#FFD700', colorName: '金黄', description: '深秋金黄的银杏大道', order: 1 },
        { name: '西溪·芦苇荡', location: { lat: 30.2710, lng: 120.0610 }, color: '#E1AD01', colorName: '芥末黄', description: '夕阳下的金色芦苇', order: 2 },
        { name: '余杭塘河·晚霞', location: { lat: 30.3080, lng: 120.0760 }, color: '#FFBF00', colorName: '琥珀', description: '河面倒映的琥珀色晚霞', order: 3 },
        { name: '龙湖·紫荆天街', location: { lat: 30.3130, lng: 120.0710 }, color: '#FFFDD0', colorName: '米黄', description: '天街的暖黄灯光夜景', order: 4 },
      ],
    }]
  }

  // 绿色系路线
  if (kw.includes('绿') || kw.includes('green') || kw.includes('自然')) {
    return [{
      title: '绿色·紫金漫步',
      description: '浙大紫金港周边的绿色角落',
      themeColor: '#7CFC00',
      points: [
        { name: '紫金港·启真湖', location: { lat: 30.3042, lng: 120.0826 }, color: '#7CFC00', colorName: '草绿', description: '启真湖畔的大草坪', order: 1 },
        { name: '西溪湿地·绿堤', location: { lat: 30.2700, lng: 120.0600 }, color: '#50C878', colorName: '翠绿', description: '湿地的翠绿水生植物', order: 2 },
        { name: '老和山', location: { lat: 30.2670, lng: 120.1290 }, color: '#808000', colorName: '橄榄绿', description: '山间的绿荫步道', order: 3 },
        { name: '余杭塘河绿道', location: { lat: 30.3090, lng: 120.0790 }, color: '#98FB98', colorName: '薄荷绿', description: '河畔的清新绿道', order: 4 },
      ],
    }]
  }

  // 默认 - 彩色路线
  return [{
    title: '彩色·紫金港色谱',
    description: '从湖水、绿道到晚霞，收集紫金港周边的颜色',
    themeColor: '#FF6B6B',
    points: [
      { name: '紫金港·南大门', location: { lat: 30.3005, lng: 120.0850 }, color: '#CC0000', colorName: '正红', description: '南大门的红色拱门', order: 1 },
      { name: '紫金港·启真湖', location: { lat: 30.3042, lng: 120.0826 }, color: '#87CEEB', colorName: '天蓝', description: '启真湖倒映的蓝天', order: 2 },
      { name: '余杭塘河绿道', location: { lat: 30.3090, lng: 120.0790 }, color: '#98FB98', colorName: '薄荷绿', description: '河畔的清新绿道', order: 3 },
      { name: '余杭塘河·晚霞', location: { lat: 30.3080, lng: 120.0760 }, color: '#FFBF00', colorName: '琥珀', description: '河面倒映的琥珀色晚霞', order: 4 },
      { name: '西溪天堂·湿地博物馆', location: { lat: 30.2690, lng: 120.0650 }, color: '#CB4154', colorName: '砖红', description: '博物馆的红砖外墙', order: 5 },
    ],
  }]
}
