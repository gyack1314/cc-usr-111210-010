# 导出事件流

EventStream消息结构为总长度u32、头长度u32、preludeCRC u32、headers、payload、messageCRC u32；总长度至少16，末CRC覆盖此前全部字节，preludeCRC只覆盖前8字节。header为u8名字字节数、UTF8名字、u8类型、值，类型0/1布尔无payload，2/3/4/5有符号8/16/32/64，6为u16长度bytes，7为u16长度UTF8，8毫秒timestamp i64，9原16字节UUID。整数均大端。重复控制头拒绝，未知名字正常保留。

Records允许空payload，CSV统一UTF8无BOM、逗号、双引号转义、CRLF记录分隔；最后一行允许无CRLF但必须闭合。CSV字段保留字符串，不把NULL变SQL null，列数不符失败，空物理行按单空字段处理而非跳过。Stats/Progress的XML在配置namespace下读取BytesScanned/BytesProcessed/BytesReturned非负整数，仅列原事件数值，不假设严格单调或必有Stats。error/exception读取:error-code/:error-message及payload保留，End无payload。

只有完整唯一End随后源EOF才成功。EOF前的全部消息都须完整校验，不能收到End就提前断开。记录来源指CSV累计payload范围及跨事件片段，不用文本字符下标当字节偏移。
