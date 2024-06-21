<!--
 * @Author: Mr.Car
 * @Date: 2024-01-24 10:31:16
-->

## 创建环境
conda env export > environment.yaml

## 恢复环境
conda env create -f environment.yaml

## 整体打包
pyinstaller -c -D --icon=icon.ico reports.py --add-data=inner\config:.\inner\config --add-data=C:\Users\Lenovo\.conda\envs\soilCli\Lib\site-packages\grapheme:grapheme --add-data=C:\Users\Lenovo\.conda\envs\soilCli\Lib\site-packages\Fiona.libs:Fiona.libs --add-data=C:\Users\Lenovo\.conda\envs\soilCli\Lib\site-packages\rasterio:rasterio
注意 pyinstaller 的更新

## 整体测试
复制如下命令：

python ./reports.py total --sample_pth test_data\sample\sample_short.shp --element_pth test_data\element\element_short.shp --suiti_pth test_data\suiti_result\suiti_result_short.shp --qual_pth test_data/quality_result/quality_short.shp --range ALL

**注意：** 上述命令中 `--range ALL` 意味着一次性生成所有成果表格
可以替换为 `--range  SAMPLE` 意味着一次性生成所有样点表格
或 `--range ELEMENT` 意味着一次性生成所有评价单元表格
或 `--range QUAL` 意味着一次性生成所有耕地质量评价表格
或 `--range SUITI` 意味着一次性生成所有适宜性评价表格

<!-- python ./reports.py total --sample_pth test_data/sample/sample_short.shp --element_pth test_data/element/element_short.shp --suiti_pth test_data/suiti_result/suiti_result_short.shp --qual_pth test_data/quality_result/quality_short.shp --range ALL -->