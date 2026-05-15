# 拾帧摄影平台 - 主页(index.html) Code Wiki

## 📋 文档概述

本文档详细说明了 `photo-manage-platform/templates/index.html` 文件中各个功能模块的实现原理、代码结构和定制方法。

---

## 🎯 页面整体结构

主页采用模块化设计，包含以下主要功能区域：

1. **Hero展示区** - 品牌宣传与主视觉
2. **平台特色介绍** - 三大核心优势展示
3. **精选作品轮播** - 景深效果3D轮播图
4. **热门作品展示** - 悬停效果图片墙
5. **最新作品推荐** - 卡片式作品列表
6. **推荐摄影师** - 索尼风格摄影师卡片
7. **公告弹窗** - 网站公告模态框
8. **页脚CTA** - 行动召唤区域

---

## 🎨 功能模块详解

### 1️⃣ Hero展示区 (第6-30行)

#### 功能说明
页面顶部的品牌宣传区域，展示平台名称和核心价值主张。

#### 代码结构

```html
<div class="showcase-container">
    <!-- 背景图片 -->
    <img src="/photo/background.jpg" alt="背景图片">
    
    <!-- 装饰性波浪图片 -->
    <img src="/photo/on.png" alt="装饰图片" class="装饰图片样式">
    
    <!-- 左侧品牌文案 -->
    <div class="品牌文案容器">
        <h1>拾帧</h1>
        <p>全国最大摄影平台</p>
        <p>分享你的每一个心动时刻</p>
    </div>
    
    <!-- 右下角作品信息 -->
    <div class="作品信息容器">
        <h5>《温馨时刻》</h5>
        <p>摄影师：小小瑶池</p>
    </div>
</div>
```

#### 样式特点
- **全屏宽度**：使用 `width: 100vw; margin-left: calc(-50vw + 50%)` 实现
- **响应式高度**：使用 `aspect-ratio: 16 / 9` 保持固定比例
- **层叠效果**：通过 `z-index` 控制文字在图片上方显示
- **文字阴影**：使用 `text-shadow` 增强可读性

#### 定制方法
- 更换背景图：修改 `src="/photo/background.jpg"`
- 调整品牌文案：编辑 `<h1>` 和 `<p>` 标签内容
- 修改字体大小：调整 `style` 中的 `font-size` 值

---

### 2️⃣ 平台特色介绍 (第34-64行)

#### 功能说明
三栏式布局展示平台的三大核心优势。

#### 代码结构

```html
<div class="py-16 bg-white mb-8">
    <div class="container">
        <h2>是什么让我们与众不同</h2>
        
        <div class="row">
            <!-- 第一栏：个人展示 -->
            <div class="col-md-4">
                <span>①</span>
                <h3>展现你自己</h3>
                <h3>寻找你的风格</h3>
                <h3>作品云盘储存</h3>
            </div>
            
            <!-- 第二栏：社区互动 -->
            <div class="col-md-4">
                <span>②</span>
                <h3>在摄影社区互动</h3>
                <h3>与全球摄影师建立联系</h3>
                <h3>提升审美与摄影技巧</h3>
            </div>
            
            <!-- 第三栏：作品价值 -->
            <div class="col-md-4">
                <span>③</span>
                <h3>发现美图获得灵感</h3>
                <h3>让作品产生价值</h3>
                <h3>让更多人理解照片价值</h3>
            </div>
        </div>
    </div>
</div>
```

#### 使用技术
- **Bootstrap Grid**：使用 `.row` 和 `.col-md-4` 实现响应式三栏布局
- **Typography**：使用 Tailwind 样式类控制字体大小和粗细

---

### 3️⃣ 精选作品轮播图 [核心功能] (第78-122行)

#### 功能说明
具有景深效果的3D轮播图，支持平滑切换、渐隐渐显动画和自动播放。

#### HTML结构

```html
<div class="custom-carousel-container">
    <div class="custom-carousel" id="customCarousel">
        <!-- 左侧导航按钮 -->
        <button class="carousel-nav-btn carousel-nav-prev" id="prevBtn">
            <svg><!-- 左箭头图标 --></svg>
        </button>
        
        <!-- 轮播轨道 -->
        <div class="carousel-track" id="carouselTrack">
            <!-- 动态生成的轮播项 -->
            {% for carousel in carousels %}
                <div class="carousel-slide" 
                     data-index="{{ loop.index0 }}"
                     data-link="{{ link_url }}"
                     data-title="{{ carousel.title }}">
                    <img src="{{ carousel.image_url }}" alt="...">
                    {% if carousel.title %}
                        <div class="carousel-slide-title">{{ carousel.title }}</div>
                    {% endif %}
                </div>
            {% endfor %}
        </div>
        
        <!-- 右侧导航按钮 -->
        <button class="carousel-nav-btn carousel-nav-next" id="nextBtn">
            <svg><!-- 右箭头图标 --></svg>
        </button>
    </div>
    
    <!-- 底部指示器点 -->
    <div class="carousel-dots" id="carouselDots">
        {% for carousel in carousels %}
            <button class="carousel-dot" data-index="{{ loop.index0 }}"></button>
        {% endfor %}
    </div>
</div>
```

#### 链接类型支持
轮播图支持四种类型的链接跳转：

| 链接类型 | 判断条件 | URL格式 |
|---------|---------|--------|
| 作品详情 | `link_type == 'work'` | `/work/detail/{id}` |
| 摄影师主页 | `link_type == 'photographer'` | `/photographer/detail/{id}` |
| 公告详情 | `link_type == 'announcement'` | `/announcement/detail/{id}` |
| 外部链接 | `link_type == 'url'` | `{link_url}` |

---

## 🎨 CSS样式详解

### 3.1 轮播图容器样式 (第144-157行)

```css
.custom-carousel-container {
    position: relative;
    padding: 60px 0;          /* 上下内边距 */
    background: #f5f5f5;        /* 浅灰色背景 */
}

.custom-carousel {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 650px;              /* 轮播图容器高度 */
    overflow: hidden;           /* 隐藏溢出内容 */
}
```

#### 设计要点
- **高度设计**：650px高度确保标题不会被遮挡
- **溢出处理**：`overflow: hidden` 隐藏切换过程中的图片

### 3.2 导航按钮样式 (第159-193行)

```css
.carousel-nav-btn {
    position: absolute;
    top: 48%;                   /* 垂直居中偏上 */
    transform: translateY(-50%);
    width: 60px;               /* 按钮宽度 */
    height: 60px;              /* 按钮高度 */
    border: none;
    background: rgba(0, 0, 0, 0.6);  /* 半透明黑色背景 */
    color: white;
    border-radius: 50%;        /* 圆形按钮 */
    cursor: pointer;
    z-index: 100;              /* 最上层显示 */
    transition: all 0.3s ease; /* 悬停动画 */
}

.carousel-nav-btn:hover {
    background: rgba(0, 0, 0, 0.8);  /* 悬停时加深背景 */
    transform: translateY(-50%) scale(1.1);  /* 放大效果 */
}

.carousel-nav-prev { left: 40px; }   /* 左侧按钮位置 */
.carousel-nav-next { right: 40px; }  /* 右侧按钮位置 */
```

#### 交互效果
- **悬停放大**：scale(1.1) 实现1.1倍放大
- **背景加深**：从60%透明度加深到80%
- **平滑过渡**：0.3秒的 ease 动画

### 3.3 轮播图片样式 (第204-284行)

#### 基础样式
```css
.carousel-slide {
    position: absolute;        /* 绝对定位 */
    display: flex;
    flex-direction: column;    /* 垂直排列：图片+标题 */
    align-items: center;
    cursor: pointer;           /* 手型光标 */
    left: 50%;
    top: 48%;                 /* 垂直位置 */
    transform: translate(-50%, -50%) scale(0.5);
    opacity: 0;                /* 默认隐藏 */
    filter: blur(10px);       /* 默认模糊 */
    z-index: 5;
    transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);  /* 关键！0.8秒过渡动画 */
}

.carousel-slide img {
    max-height: 420px;        /* 最大高度 */
    max-width: 630px;         /* 最大宽度 */
    width: auto;
    height: auto;
    object-fit: contain;      /* 保持原始比例 */
    border-radius: 12px;      /* 圆角 */
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);  /* 阴影 */
}

.carousel-slide-title {
    margin-top: 18px;
    color: #333;
    font-weight: 600;
    font-size: 1.1rem;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
}
```

#### 景深位置样式

| 位置类 | left值 | scale | opacity | blur | z-index | 说明 |
|-------|--------|-------|---------|------|---------|------|
| `.position-prev` | 15% | 0.7 | 0.5 | 3px | 10 | 左侧景深 |
| `.position-current` | 50% | 1.05 | 1 | 0 | 50 | 中间主图 |
| `.position-next` | 85% | 0.7 | 0.5 | 3px | 10 | 右侧景深 |
| `.position-hidden-left` | -20% | 0.5 | 0 | 10px | 5 | 左隐藏 |
| `.position-hidden-right` | 120% | 0.5 | 0 | 10px | 5 | 右隐藏 |

#### 景深效果原理

1. **缩放效果**：
   - 主图：scale(1.05) - 1.05倍大小
   - 景深图：scale(0.7) - 0.7倍大小（缩小35%）
   - 隐藏图：scale(0.5) - 0.5倍大小（缩小50%）

2. **模糊效果**：
   - 主图：blur(0) - 完全清晰
   - 景深图：blur(3px) - 轻度模糊
   - 隐藏图：blur(10px) - 重度模糊

3. **透明度效果**：
   - 主图：opacity: 1 - 完全不透明
   - 景深图：opacity: 0.5 - 50%透明度
   - 隐藏图：opacity: 0 - 完全透明

#### 渐隐渐显动画机制

```css
/* 所有变换属性都应用相同的过渡时间 */
.carousel-slide {
    transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
```

**关键点**：
- **统一过渡时间**：所有属性（left、scale、opacity、filter）都是0.8秒
- **贝塞尔曲线**：`cubic-bezier(0.4, 0, 0.2, 1)` 提供平滑的加速减速效果
- **延迟初始化**：JavaScript中使用setTimeout确保CSS先渲染再应用类名

### 3.4 底部指示器样式 (第286-310行)

```css
.carousel-dots {
    display: flex;
    justify-content: center;
    gap: 12px;                /* 点之间间距 */
    margin-top: 30px;
}

.carousel-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;       /* 圆形点 */
    border: none;
    background: #ccc;         /* 默认灰色 */
    cursor: pointer;
    transition: all 0.3s ease;
}

.carousel-dot:hover {
    background: #999;         /* 悬停时变深 */
}

.carousel-dot.active {
    background: #333;         /* 激活状态黑色 */
    transform: scale(1.2);     /* 放大20% */
}
```

---

## ⚙️ JavaScript交互逻辑

### 核心功能实现 (第623-723行)

#### 1. 初始化与状态管理

```javascript
let currentIndex = 0;          // 当前显示的图片索引
const totalSlides = slides.length;  // 总图片数
let isAnimating = false;       // 动画锁，防止重复点击
let isInitialized = false;      // 初始化标志
```

#### 2. 核心函数：updateSlides()

```javascript
function updateSlides() {
    slides.forEach((slide, index) => {
        // 移除所有位置类
        slide.classList.remove(
            'position-prev',
            'position-current',
            'position-next',
            'position-hidden-left',
            'position-hidden-right'
        );
        
        // 计算当前位置与目标位置的差值
        let diff = index - currentIndex;
        
        // 环形数组处理（处理首尾循环）
        if (diff > totalSlides / 2) {
            diff = diff - totalSlides;
        } else if (diff < -totalSlides / 2) {
            diff = diff + totalSlides;
        }
        
        // 根据差值分配位置类
        if (diff === -1) {
            slide.classList.add('position-prev');      // 左侧景深
        } else if (diff === 0) {
            slide.classList.add('position-current');    // 中间主图
        } else if (diff === 1) {
            slide.classList.add('position-next');       // 右侧景深
        } else if (diff < -1) {
            slide.classList.add('position-hidden-left'); // 左隐藏
        } else {
            slide.classList.add('position-hidden-right'); // 右隐藏
        }
    });
    
    // 更新指示器点
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentIndex);
    });
}
```

**算法说明**：
- **差值计算**：计算当前索引与目标索引的差
- **环形处理**：当差值超过总数的一半时，调整差值确保最短路径
- **类名分配**：根据差值分配对应的CSS类

#### 3. 图片切换函数

```javascript
function goToSlide(index) {
    // 防止动画过程中重复点击
    if (isAnimating || index === currentIndex) return;
    
    isAnimating = true;           // 锁定动画
    currentIndex = index;         // 更新当前索引
    updateSlides();               // 执行位置更新
    
    // 800ms后解锁（与CSS transition时间一致）
    setTimeout(() => {
        isAnimating = false;
    }, 800);
}

function nextSlide() {
    // 循环切换到下一张
    const newIndex = (currentIndex + 1) % totalSlides;
    goToSlide(newIndex);
}

function prevSlide() {
    // 循环切换到上一张
    const newIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    goToSlide(newIndex);
}
```

#### 4. 事件绑定

```javascript
// 导航按钮点击事件
prevBtn.addEventListener('click', prevSlide);
nextBtn.addEventListener('click', nextSlide);

// 指示器点点击事件
dots.forEach((dot, index) => {
    dot.addEventListener('click', () => goToSlide(index));
});

// 图片点击跳转
slides.forEach(slide => {
    slide.addEventListener('click', function() {
        const link = this.getAttribute('data-link');
        if (link) {
            window.location.href = link;
        }
    });
});
```

#### 5. 自动播放功能

```javascript
let autoPlayInterval;

function startAutoPlay() {
    // 每5秒自动切换到下一张
    autoPlayInterval = setInterval(nextSlide, 5000);
}

function stopAutoPlay() {
    clearInterval(autoPlayInterval);
}

// 鼠标悬停暂停，离开继续
const carousel = document.getElementById('customCarousel');
carousel.addEventListener('mouseenter', stopAutoPlay);
carousel.addEventListener('mouseleave', startAutoPlay);

// 延迟初始化，确保CSS先渲染
requestAnimationFrame(() => {
    setTimeout(() => {
        updateSlides();
        isInitialized = true;
        startAutoPlay();
    }, 50);
});
```

---

## 📦 其他功能模块

### 4️⃣ 热门作品展示 (第312-417行)

#### 功能特点
- 响应式网格布局
- 图片悬停放大效果
- 渐变遮罩层显示标题和作者

#### 核心代码

```html
<div class="hot-works-container">
    {% for work in hot_works %}
        <div class="hot-work-item">
            <a href="/work/detail/{{ work.work_id }}" class="hot-work-link">
                <div class="hot-work-image-wrapper">
                    <img src="{{ images[0].image_url }}" alt="{{ work.title }}">
                </div>
                <!-- 悬停遮罩 -->
                <div class="hot-work-overlay">
                    <div class="hot-work-title">{{ work.title }}</div>
                    <div class="hot-work-author">摄影师：{{ work.photographer.user.nickname }}</div>
                </div>
                <!-- 多图指示 -->
                {% if images|length > 1 %}
                    <span class="hot-work-more-indicator">+{{ images|length - 1 }} 张</span>
                {% endif %}
            </a>
        </div>
    {% endfor %}
</div>
```

#### CSS交互

```css
/* 悬停放大效果 */
.hot-work-item:hover .hot-work-image-wrapper img {
    transform: scale(1.05);
}

/* 悬停显示遮罩 */
.hot-work-item:hover .hot-work-overlay {
    opacity: 1;
}
```

---

### 5️⃣ 最新作品卡片 (第434-449行)

#### 功能特点
- Bootstrap卡片组件
- 固定高度缩略图
- 日期显示和查看按钮

```html
<div class="card h-full border-0 shadow-md rounded-xl overflow-hidden">
    <img src="{{ work.cover_url }}" class="card-img-top" style="height: 180px; object-fit: cover;">
    <div class="card-body">
        <h5 class="card-title">{{ work.title }}</h5>
        <p class="card-text">{{ work.create_time.strftime('%Y-%m-%d') }}</p>
        <a href="/work/detail/{{ work.work_id }}" class="btn">查看</a>
    </div>
</div>
```

---

### 6️⃣ 推荐摄影师卡片 (第470-560行)

#### 功能特点
- 索尼风格设计
- 头像+作品网格展示
- 瀑布流布局（第一张图片跨两行）

#### 网格布局

```css
.sony-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;  /* 三列等宽 */
    gap: 6px;                            /* 6px间距 */
}

.sony-grid .big-img {
    grid-row: span 2;  /* 第一张图片跨两行 */
}
```

#### 数据筛选
```jinja2
{% set valid_works = photographer.works | selectattr('status', 'equalto', 1) | list %}
```

仅显示状态为1（已上架）的作品。

---

### 7️⃣ 公告弹窗 (第566-592行)

#### 功能说明
网站公告模态框，支持"不再弹出"功能。

#### 关键特性
- **首次弹窗**：使用 localStorage 记录用户选择
- **延迟显示**：等待页面加载完成后显示
- **内容预览**：显示前180个字符

#### 核心代码

```javascript
var announcementId = modalElement.getAttribute('data-announcement-id');
var storageKey = 'hiddenAnnouncement:' + announcementId;

// 检查是否已选择"不再弹出"
if (localStorage.getItem(storageKey)) {
    return;  // 不显示弹窗
}

var announcementModal = new bootstrap.Modal(modalElement);
announcementModal.show();

// 保存用户选择
modalElement.addEventListener('hidden.bs.modal', function() {
    if (skipCheckbox.checked) {
        localStorage.setItem(storageKey, '1');
    }
});
```

---

### 8️⃣ 页脚CTA区域 (第727-752行)

```html
<div class="加入我们容器">
    <h2>加入我们</h2>
    <p>Everything is possible!</p>
</div>
```

#### 样式特点
- 全宽背景色：#4B4B8A（紫色）
- 固定内边距：80px上下
- 响应式居中对齐

---

## 🔧 定制指南

### 修改轮播图动画时间

```css
.carousel-slide {
    /* 修改这里的0.8s为其他值 */
    transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
```

**JavaScript中同步修改**：
```javascript
setTimeout(() => {
    isAnimating = false;
}, 800);  // 这里的800ms需要与CSS一致
```

### 修改景深效果强度

```css
/* 景深图片样式 */
.carousel-slide.position-prev {
    transform: translate(-50%, -50%) scale(0.7);  /* 缩小到70% */
    opacity: 0.5;                                  /* 50%透明度 */
    filter: blur(3px);                            /* 3px模糊 */
}
```

### 修改自动播放间隔

```javascript
function startAutoPlay() {
    // 修改5000为其他毫秒值（如3000为3秒）
    autoPlayInterval = setInterval(nextSlide, 5000);
}
```

### 修改主图尺寸

```css
.carousel-slide img {
    max-height: 420px;   /* 最大高度 */
    max-width: 630px;     /* 最大宽度 */
}

.carousel-slide.position-current {
    transform: translate(-50%, -50%) scale(1.05);  /* 主图缩放倍数 */
}
```

---

## 📊 技术栈总结

| 技术 | 用途 | 文档参考 |
|------|------|----------|
| **Jinja2** | 模板引擎，数据动态渲染 | [官方文档](https://jinja.palletsprojects.com/) |
| **Bootstrap 5** | 响应式布局和基础组件 | [官方文档](https://getbootstrap.com/docs/5.0/) |
| **CSS Transitions** | 平滑动画过渡效果 | [MDN文档](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Transitions) |
| **CSS Grid** | 摄影师卡片网格布局 | [MDN文档](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Grid_Layout) |
| **Flexbox** | 弹性盒模型布局 | [MDN文档](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Flexible_Box_Layout) |
| **Vanilla JavaScript** | 轮播图交互逻辑 | [官方文档](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript) |
| **localStorage** | 公告弹窗记忆功能 | [MDN文档](https://developer.mozilla.org/zh-CN/docs/Web/API/Window/localStorage) |

---

## 🎯 性能优化建议

1. **图片优化**
   - 使用 WebP 格式减少文件大小
   - 实现图片懒加载
   - 添加适当的 `loading="lazy"` 属性

2. **动画优化**
   - 使用 `transform` 和 `opacity` 实现GPU加速
   - 避免使用 `layout` 属性进行动画（如 `width`、`height`）

3. **JavaScript优化**
   - 使用事件委托减少事件监听器数量
   - 节流处理高频事件（如窗口resize）

---

## 📝 维护记录

| 日期 | 修改内容 | 修改人 |
|------|---------|--------|
| 2026-05-15 | 实现景深效果3D轮播图 | AI Assistant |
| 2026-05-15 | 添加渐隐渐显动画效果 | AI Assistant |
| 2026-05-15 | 优化图片位置，解决显示问题 | AI Assistant |
| 2026-05-15 | 修复景深图片切换平滑度 | AI Assistant |
| 2026-05-15 | 调整图片尺寸，解决标题遮挡 | AI Assistant |

---

## ❓ 常见问题

### Q: 如何禁用自动播放？
**A:** 删除或注释 `startAutoPlay()` 调用：
```javascript
// startAutoPlay();  // 注释掉这行
```

### Q: 如何只显示2张图片？
**A:** 在后端查询时添加 `.limit(2)` 限制返回数量。

### Q: 图片模糊效果太强怎么办？
**A:** 调整CSS中的 `blur()` 值：
```css
.carousel-slide.position-prev {
    filter: blur(3px);  /* 减小模糊值 */
}
```

### Q: 如何添加自定义过渡动画？
**A:** 使用 `cubic-bezier()` 生成自定义缓动函数：
- 线性：`cubic-bezier(0, 0, 1, 1)`
- 加速：`cubic-bezier(0.4, 0, 1, 1)`
- 减速：`cubic-bezier(0, 0, 0.2, 1)`

---

## 📚 相关资源

- **项目仓库**：`photo-manage-platform`
- **模板文件**：`templates/index.html`
- **基础模板**：`templates/base.html`
- **轮播模型**：`models/Carousel.py`
- **轮播视图**：`views/carousel.py`

---

*本文档最后更新于 2026-05-15*
