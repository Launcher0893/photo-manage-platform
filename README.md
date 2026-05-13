# photo-manage-platfrom

摄影作品分享平台 Flask 课程项目。

## 运行说明

- 当前默认数据库为本机 MySQL：`photo_manage_platform`
- 默认连接串在 [config.py](./config.py) 中，直接运行 `python app.py` 会连接：
  `mysql+pymysql://root:Sean20041218@127.0.0.1:3306/photo_manage_platform?charset=utf8mb4`
- 如果需要覆盖默认数据库，设置环境变量 `DATABASE_URL` 即可
- 首次运行前需要先将 [photo_manage_platform.sql](./photo_manage_platform.sql) 导入 MySQL
