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
 * 返回匹配结果的元信息（视频来源、匹配标签等）
 */
export interface RouteMatchMeta {
  /** 匹配的视频链接 */
  sourceUrl: string
  /** 展示标签（如"故宫 · 红色系"） */
  label: string
  /** 简短描述 */
  hint: string
}

/**
 * 扩展的路线建议（含匹配信息）
 */
export interface ColorRouteSuggestionWithMeta extends ColorRouteSuggestion {
  meta?: RouteMatchMeta
}

// ============================================================
// 硬编码 Demo 数据
// ============================================================

const DEMO_ROUTES: { urls: string[]; kw: string[]; route: ColorRouteSuggestion; meta?: RouteMatchMeta }[] = [
  // ---- 绿色系 · 紫金漫步 ----
  {
    urls: [],
    kw: ['绿', 'green', '自然', '紫金港'],
    route: {

      title: '绿色·紫金漫步',
      description: '浙大紫金港周边的绿色角落',
      themeColor: '#7CFC00',
      points: [
        { name: '紫金港·启真湖', location: { lat: 30.3042, lng: 120.0826 }, color: '#7CFC00', colorName: '草绿', description: '启真湖畔的大草坪', order: 1 },
        { name: '西溪湿地·绿堤', location: { lat: 30.2700, lng: 120.0600 }, color: '#50C878', colorName: '翠绿', description: '湿地的翠绿水生植物', order: 2 },
        { name: '老和山', location: { lat: 30.2670, lng: 120.1290 }, color: '#808000', colorName: '橄榄绿', description: '山间的绿荫步道', order: 3 },
        { name: '余杭塘河绿道', location: { lat: 30.3090, lng: 120.0790 }, color: '#98FB98', colorName: '薄荷绿', description: '河畔的清新绿道', order: 4 },
      ],
    },
  },

  // ---- 红色系 · 紫金印象 ----
  {
    urls: [],
    kw: ['红', 'red', '热烈', '紫金港'],
    route: {
      title: '红色·紫金印象',
      description: '从西溪到紫金港，寻一抹红色',
      themeColor: '#FF0000',
      points: [
        { name: '紫金港·南大门', location: { lat: 30.3005, lng: 120.0850 }, color: '#CC0000', colorName: '正红', description: '南大门的红色拱门', order: 1 },
        { name: '西溪·梅林', location: { lat: 30.2720, lng: 120.0580 }, color: '#E34234', colorName: '朱红', description: '冬日盛开的红色梅花', order: 2 },
        { name: '西溪天堂·湿地博物馆', location: { lat: 30.2690, lng: 120.0650 }, color: '#CB4154', colorName: '砖红', description: '博物馆的红砖外墙', order: 3 },
        { name: '三墩老街·夕照', location: { lat: 30.3180, lng: 120.0680 }, color: '#800020', colorName: '酒红', description: '老街黄昏的酒红色余晖', order: 4 },
      ],
    },
  },

  // ---- 金色系 · 西溪秋韵 ----
  {
    urls: [],
    kw: ['黄', '金', 'yellow', '温暖', '西溪', '秋'],
    route: {
      title: '金色·西溪秋韵',
      description: '紫金港周边的金色光影',
      themeColor: '#FFD700',
      points: [
        { name: '紫金港·银杏大道', location: { lat: 30.3030, lng: 120.0840 }, color: '#FFD700', colorName: '金黄', description: '深秋金黄的银杏大道', order: 1 },
        { name: '西溪·芦苇荡', location: { lat: 30.2710, lng: 120.0610 }, color: '#E1AD01', colorName: '芥末黄', description: '夕阳下的金色芦苇', order: 2 },
        { name: '余杭塘河·晚霞', location: { lat: 30.3080, lng: 120.0760 }, color: '#FFBF00', colorName: '琥珀', description: '河面倒映的琥珀色晚霞', order: 3 },
        { name: '龙湖·紫荆天街', location: { lat: 30.3130, lng: 120.0710 }, color: '#FFFDD0', colorName: '米黄', description: '天街的暖黄灯光夜景', order: 4 },
      ],
    },
  },

  // ---- 蓝色系 · 启真水色 ----
  {
    urls: [],
    kw: ['蓝', 'blue', '清新', '启真湖', '水'],
    route: {
      title: '蓝色·启真水色',
      description: '紫金港周边的蓝色水系',
      themeColor: '#4B9FE3',
      points: [
        { name: '紫金港·启真湖', location: { lat: 30.3042, lng: 120.0826 }, color: '#87CEEB', colorName: '天蓝', description: '启真湖倒映的蓝天', order: 1 },
        { name: '西溪·湿地湖泊', location: { lat: 30.2705, lng: 120.0590 }, color: '#30D5C8', colorName: '湖蓝', description: '湿地湖面的清透蓝色', order: 2 },
        { name: '余杭塘河', location: { lat: 30.3090, lng: 120.0790 }, color: '#4B0082', colorName: '靛蓝', description: '河水的靛蓝色调', order: 3 },
        { name: '紫金港·蓝桥', location: { lat: 30.3055, lng: 120.0835 }, color: '#0047AB', colorName: '钴蓝', description: '校园蓝桥的钴蓝栏杆', order: 4 },
      ],
    },
  },

  // ---- Demo 1: 故宫（红色系）----
  {
    urls: [
      'douyin.com/video/7589575665189766907',
      'v.douyin.com/7589575665189766907',
    ],
    kw: ['故宫', '红色', '京城'],
    meta: {
      sourceUrl: 'https://www.douyin.com/video/7589575665189766907',
      label: '故宫 · 红色系',
      hint: '春日故宫 vlog，从午门到御花园，一路中国红',
    },
    route: {
      title: '红色·故宫皇城',
      description: '午门 → 太和殿 → 御花园 → 景山，收集故宫的红色',
      themeColor: '#CC0000',
      points: [
        { name: '故宫午门', location: { lat: 39.9147, lng: 116.3956 }, color: '#CC0000', colorName: '正红', description: '午门的正红城墙，故宫最标志性的红色', order: 1 },
        { name: '太和殿', location: { lat: 39.9155, lng: 116.3970 }, color: '#E34234', colorName: '朱红', description: '太和殿朱红立柱与金色匾额', order: 2 },
        { name: '红墙夹道', location: { lat: 39.9170, lng: 116.3940 }, color: '#CB4154', colorName: '砖红', description: '东西六宫之间的红色夹道', order: 3 },
        { name: '御花园', location: { lat: 39.9195, lng: 116.3975 }, color: '#FF007F', colorName: '玫瑰红', description: '御花园古树与宫墙的玫瑰色调', order: 4 },
        { name: '景山万春亭', location: { lat: 39.9225, lng: 116.3966 }, color: '#800020', colorName: '酒红', description: '景山俯瞰故宫全景，落日酒红', order: 5 },
      ],
    },
  },

  // ---- Demo 2: 西湖（蓝绿色系）----
  {
    urls: [
      'v.douyin.com/fGdzve7K6kg',
      'douyin.com/video/fGdzve7K6kg',
    ],
    kw: ['西湖', '蓝', '绿', '杭州', '湖'],
    meta: {
      sourceUrl: 'https://v.douyin.com/fGdzve7K6kg/',
      label: '西湖 · 蓝绿色系',
      hint: '西湖美景航拍，断桥、苏堤、湖面，湖蓝与草绿',
    },
    route: {
      title: '蓝绿·西湖漫步',
      description: '断桥 → 白堤 → 苏堤 → 湖心亭 → 雷峰塔，水色与山色',
      themeColor: '#30D5C8',
      points: [
        { name: '断桥', location: { lat: 30.2630, lng: 120.1510 }, color: '#87CEEB', colorName: '天蓝', description: '断桥残雪，桥拱映蓝天', order: 1 },
        { name: '白堤', location: { lat: 30.2590, lng: 120.1480 }, color: '#98FB98', colorName: '薄荷绿', description: '白堤春柳，嫩绿拂水', order: 2 },
        { name: '苏堤', location: { lat: 30.2480, lng: 120.1390 }, color: '#7CFC00', colorName: '草绿', description: '苏堤春晓，六桥烟柳', order: 3 },
        { name: '湖心亭', location: { lat: 30.2550, lng: 120.1420 }, color: '#30D5C8', colorName: '湖蓝', description: '湖心亭远眺，湖面如镜', order: 4 },
        { name: '雷峰塔', location: { lat: 30.2390, lng: 120.1480 }, color: '#50C878', colorName: '翠绿', description: '雷峰夕照，塔影入翠湖', order: 5 },
      ],
    },
  },

  // ---- Demo 3: 地坛银杏（金色系）----
  {
    urls: [
      'douyin.com/video/7570485729290247865',
      'v.douyin.com/7570485729290247865',
    ],
    kw: ['地坛', '银杏', '金', '黄', '秋'],
    meta: {
      sourceUrl: 'https://www.douyin.com/video/7570485729290247865',
      label: '地坛 · 金色系',
      hint: '地坛公园银杏大道 vlog，金黄银杏叶，满目金色',
    },
    route: {
      title: '金色·地坛秋韵',
      description: '地坛公园银杏大道，收集北京秋天的金色',
      themeColor: '#FFD700',
      points: [
        { name: '地坛南门', location: { lat: 39.9520, lng: 116.4100 }, color: '#E1AD01', colorName: '芥末黄', description: '地坛南门的红墙与黄叶', order: 1 },
        { name: '银杏大道', location: { lat: 39.9540, lng: 116.4110 }, color: '#FFD700', colorName: '金黄', description: '银杏大道，满树金黄', order: 2 },
        { name: '方泽坛', location: { lat: 39.9530, lng: 116.4090 }, color: '#FFBF00', colorName: '琥珀', description: '方泽坛前的金色阳光', order: 3 },
        { name: '牡丹园', location: { lat: 39.9550, lng: 116.4120 }, color: '#FFFDD0', colorName: '米黄', description: '秋日牡丹园柔和米黄', order: 4 },
        { name: '地坛北门', location: { lat: 39.9560, lng: 116.4110 }, color: '#FBCEB1', colorName: '杏色', description: '北门出口的暖杏色余晖', order: 5 },
      ],
    },
  },
]

/**
 * 解析用户输入，返回颜色路线建议
 *
 * 1. 优先匹配抖音视频链接（硬编码 Demo 数据）
 * 2. 其次按关键词匹配
 * 3. 默认返回彩色综合路线
 */
export function parseRouteInput(input: string): ColorRouteSuggestionWithMeta[] {
  const trimmed = input.trim()
  const kw = trimmed.toLowerCase()

  // 1. 按抖音链接匹配
  for (const demo of DEMO_ROUTES) {
    if (demo.urls.some((url) => kw.includes(url))) {
      return [{ ...demo.route, meta: demo.meta }]
    }
  }

  // 2. 按关键词匹配
  for (const demo of DEMO_ROUTES) {
    if (demo.kw.some((k) => kw.includes(k))) {
      return [{ ...demo.route, meta: demo.meta }]
    }
  }

  // 3. 默认 - 彩色综合路线（紫金港周边）
  return [{
    title: '彩色·紫金万象',
    description: '从启真湖到西溪，收集紫金港的颜色',
    themeColor: '#FF6B6B',
    points: [
      { name: '紫金港·南大门', location: { lat: 30.3005, lng: 120.0850 }, color: '#CC0000', colorName: '正红', description: '南大门的红色拱门', order: 1 },
      { name: '启真湖', location: { lat: 30.3042, lng: 120.0826 }, color: '#87CEEB', colorName: '天蓝', description: '启真湖倒映蓝天', order: 2 },
      { name: '银杏大道', location: { lat: 30.3030, lng: 120.0840 }, color: '#FFD700', colorName: '金黄', description: '深秋银杏金黄大道', order: 3 },
      { name: '西溪湿地·绿堤', location: { lat: 30.2700, lng: 120.0600 }, color: '#7CFC00', colorName: '草绿', description: '湿地翠绿水生植物', order: 4 },
      { name: '紫金港·蓝桥', location: { lat: 30.3055, lng: 120.0835 }, color: '#8F00FF', colorName: '紫罗兰', description: '蓝桥旁的紫霞', order: 5 },
    ],
  }]
}
