/**
 * 颜色旅行路径系统类型定义
 *
 * 接口说明（供明日硬编码对接用）：
 *   parseRouteInput(input)  → ColorRouteSuggestion[]
 *   输入抖音链接或文字，返回一组颜色路线建议
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
  /** 交给明日硬编码映射：返回 ColorRouteSuggestion[] */
  suggestions: ColorRouteSuggestion[]
}

// ============================================================
// 明日对接接口：替换此函数的实现即可
// ============================================================

/**
 * 解析用户输入，返回颜色路线建议
 *
 * 演示数据：按关键词返回预设路线。
 * 明日替换为端对端硬编码映射（抖音链接 → 颜色点位）。
 */
export function parseRouteInput(input: string): ColorRouteSuggestion[] {
  const kw = input.toLowerCase()

  // 红色系路线
  if (kw.includes('红') || kw.includes('red') || kw.includes('热烈')) {
    return [{
      title: '红色·京城中轴线',
      description: '从故宫到前门，一路中国红',
      themeColor: '#FF0000',
      points: [
        { name: '故宫午门', location: { lat: 39.9147, lng: 116.3956 }, color: '#CC0000', colorName: '正红', description: '故宫的正红城墙', order: 1 },
        { name: '天安门', location: { lat: 39.9054, lng: 116.3976 }, color: '#E34234', colorName: '朱红', description: '天安门城楼', order: 2 },
        { name: '前门大街', location: { lat: 39.8950, lng: 116.3960 }, color: '#CB4154', colorName: '砖红', description: '前门的砖红色建筑', order: 3 },
        { name: '永定门', location: { lat: 39.8708, lng: 116.3942 }, color: '#800020', colorName: '酒红', description: '永定门城楼', order: 4 },
      ],
    }]
  }

  // 蓝色系路线
  if (kw.includes('蓝') || kw.includes('blue') || kw.includes('清新')) {
    return [{
      title: '蓝色·水畔漫步',
      description: '沿着北京的水系寻找蓝色',
      themeColor: '#4B9FE3',
      points: [
        { name: '北海公园', location: { lat: 39.9243, lng: 116.3893 }, color: '#87CEEB', colorName: '天蓝', description: '北海的白塔与蓝天', order: 1 },
        { name: '后海', location: { lat: 39.9400, lng: 116.3840 }, color: '#30D5C8', colorName: '湖蓝', description: '后海的湖面', order: 2 },
        { name: '颐和园昆明湖', location: { lat: 39.9998, lng: 116.2755 }, color: '#4B0082', colorName: '靛蓝', description: '昆明湖的靛蓝倒影', order: 3 },
        { name: '国家大剧院', location: { lat: 39.9030, lng: 116.3833 }, color: '#0047AB', colorName: '钴蓝', description: '大剧院的蓝色玻璃幕墙', order: 4 },
      ],
    }]
  }

  // 黄色/金色系路线
  if (kw.includes('黄') || kw.includes('金') || kw.includes('yellow') || kw.includes('温暖')) {
    return [{
      title: '金色·夕阳古都',
      description: '日落时分，北京的金色时刻',
      themeColor: '#FFD700',
      points: [
        { name: '景山万春亭', location: { lat: 39.9225, lng: 116.3966 }, color: '#FFD700', colorName: '金黄', description: '俯瞰故宫全景', order: 1 },
        { name: '天坛祈年殿', location: { lat: 39.8822, lng: 116.4066 }, color: '#E1AD01', colorName: '芥末黄', description: '祈年殿的金色宝顶', order: 2 },
        { name: '鼓楼', location: { lat: 39.9397, lng: 116.4040 }, color: '#FFFDD0', colorName: '米黄', description: '鼓楼的暖黄灯光', order: 3 },
        { name: '国贸CBD', location: { lat: 39.9087, lng: 116.4605 }, color: '#FFBF00', colorName: '琥珀', description: '国贸的落日余晖', order: 4 },
      ],
    }]
  }

  // 绿色系路线
  if (kw.includes('绿') || kw.includes('green') || kw.includes('自然')) {
    return [{
      title: '绿色·城市绿洲',
      description: '北京的绿色角落与公园',
      themeColor: '#7CFC00',
      points: [
        { name: '奥森公园', location: { lat: 40.0150, lng: 116.3900 }, color: '#7CFC00', colorName: '草绿', description: '奥林匹克森林公园', order: 1 },
        { name: '中山公园', location: { lat: 39.9086, lng: 116.3972 }, color: '#50C878', colorName: '翠绿', description: '古树参天', order: 2 },
        { name: '颐和园', location: { lat: 40.0010, lng: 116.2770 }, color: '#808000', colorName: '橄榄绿', description: '万寿山的绿荫', order: 3 },
        { name: '紫竹院公园', location: { lat: 39.9420, lng: 116.3160 }, color: '#98FB98', colorName: '薄荷绿', description: '竹林小径', order: 4 },
      ],
    }]
  }

  // 默认 - 彩色路线
  return [{
    title: '彩色·北京色谱',
    description: '从红到紫，收集北京的颜色',
    themeColor: '#FF6B6B',
    points: [
      { name: '故宫', location: { lat: 39.9147, lng: 116.3956 }, color: '#CC0000', colorName: '正红', description: '故宫红墙', order: 1 },
      { name: '天坛', location: { lat: 39.8822, lng: 116.4066 }, color: '#0047AB', colorName: '钴蓝', description: '天坛蓝瓦', order: 2 },
      { name: '北海公园', location: { lat: 39.9243, lng: 116.3893 }, color: '#7CFC00', colorName: '草绿', description: '北海绿柳', order: 3 },
      { name: '鼓楼', location: { lat: 39.9397, lng: 116.4040 }, color: '#FFD700', colorName: '金黄', description: '鼓楼夕照', order: 4 },
      { name: '颐和园', location: { lat: 39.9998, lng: 116.2755 }, color: '#8F00FF', colorName: '紫罗兰', description: '颐和园紫霞', order: 5 },
    ],
  }]
}
