---
title: "C++ MFC：优雅的 DEBUG 方式 & 解决注册表读写问题"
layout: post
date: 2019-12-16
tag:
- C++
- Debug
category: blog
author: ingerchao
---


**C++ 中 MFC 应用程序优雅的 debug 方式**：让exe在启动时同时启动一个控制台，在控制台中使用 cout 或 printf 对程序中的值进行 debug。

![1576503344334](./../assets\images\program\bolt/1576503344334.png)

修改项目属性后期生成事件的命令行值为：`editbin /SUBSYSTEM:CONSOLE $(OUTDIR)\$(ProjectName).exe`.

![MFC DEBUG](./../assets\images\program\bolt/1576503427125.png)

C++读取从注册表中读取 Autocad 安装路径，使用 `RegOpenKeyEx` 方法打开注册表，根据方法的返回值判断是否打开成功，然后使用`RegQueryValueEx`方法读取 key 的 value 值，判断此方法的返回值判断是否读取成功， 若成功返回 value值。

**注意：** 使用 RegOpenKeyEx 方法在指定第四个参数打开方式时 64 位机器必须加入参数 `KEY_WOW64_64KEY` ，否则会调用该方法会返回错误值 **2**。 

![1576502674386](./../assets\images\program\bolt/1576502674386.png)

```c++

CString CFileUtil::GetAppRegeditPath()
{
	
	 CString strAppName("SOFTWARE\\Autodesk\\AutoCAD\\R21.0\\ACAD-0001:804");
	std::cout << strAppName.GetString() << std::endl;
	HKEY hKey;
	CString strAppRegeditPath("");
	TCHAR szProductType[MAX_PATH];
	memset(szProductType, 0, sizeof(szProductType));

	DWORD dwBuflen = MAX_PATH;
	LONG lRet = 0;

	// 打开注册表，只有打开后才能进行其他操作
	lRet = RegOpenKeyEx(HKEY_LOCAL_MACHINE, //要打开的根键
		LPCTSTR(strAppName), // 要打开的子键
		0, //这个一定为0
		KEY_WOW64_64KEY | KEY_QUERY_VALUE,//指定打开方式为读
		&hKey
	);

	std::cout << "lret: " << lRet << std::endl;
	if (lRet != ERROR_SUCCESS)
	{
		printf("open error!\n");
		return strAppRegeditPath;
	}
	else
	{
		// 下面开始查询
		lRet = RegQueryValueEx(hKey, //打开注册表时返回的句柄
			TEXT("AcadLocation"), //要查询的名称
			NULL, NULL,
			(LPBYTE)szProductType,
			&dwBuflen);
	}
	if (lRet != ERROR_SUCCESS)
	{
		printf("read error!\n");

		return strAppRegeditPath;
	}
	else
	{
		RegCloseKey(hKey);
		strAppRegeditPath = szProductType;

	}
	return strAppRegeditPath;
}

```

![1576503143373](./../assets\images\program\bolt/1576503143373.png)

