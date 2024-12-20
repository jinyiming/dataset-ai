
### 关键技术设计

前后端分离
采用前后端分离架构中，后端只需要负责按照约定的数据格式向前端提供可调用的API服务即可。前后端之间通过HTTP请求进行交互，前端获取到数据后，进行页面的装配和渲染。前后端分离通过前端静态化、后端数据化、平台无关化、构架无关化使得前后端交互流量大幅减少，表现性能大幅提升；前后台技术无关性具备更优的平台兼容特性，后端应用统一控制安全以及业务处理逻辑保证安全和业务处理一致；前后端合理分工提升开发效率易于平台是迁移实施。
高性能设计
针对基于国产化应用的高性能需求，评估系统性能预期，自底向上分层解决。基于目前运行的系统，对未来可能发生的系统并发数据进行估算，以保证系统性能设计的阀值满足办公平台云部署后系统正常、高效运行需求。
1．在操作系统层面，可以对操作系统参数进行优化调整；
2．在服务器层面（应用服务器和数据库服务器），可以对服务器参数进行调优；
3．在系统架构层面，可以从动态数据缓存、动静态内容分离、动态内容静态化、JS压缩、传输压缩等方面进行调优；
4．在业务逻辑层次，可以通过深化分析、优化业务逻辑、简化业务操作进行性能调优；
5．在应用逻辑方面，可以对执行效率不高的代码进行针对性优化。
