<!--
 * @Author: Mr.Car
 * @Date: 2024-01-24 10:31:16
-->

## 创建环境
conda env export > environment.yaml

## 恢复环境
conda env create -f environment.yaml

## 整体打包
pyinstaller -c -D --icon=icon.ico reports.py --add-data=config:./config --add-data=C:\Users\Lenovo\.conda\envs\soilCli\Lib\site-packages\grapheme:grapheme --add-data=C:\Users\Lenovo\.conda\envs\soilCli\Lib\site-packages\Fiona.libs:Fiona.libs --add-data=C:\Users\Lenovo\.conda\envs\soilCli\Lib\site-packages\rasterio:rasterio
注意 pyinstaller 的更新

## 整体测试
复制如下命令：

python ./reports.py total --sample_pth test_data\sample\sample_short.shp --element_pth test_data\element\element_short.shp --suti_pth test_data\suiti_result\suiti_result_short.shp --qual_pth test_data/quality_result/quality_short.shp --type_list "['JSBG_7','JSBG_8','TRSX_111','QUAL_76_78','QUAL_77','QUAL_72','QUAL_73','QUAL_74','QUAL_75','SUITI']"


<!-- python ./reports.py total --sample_pth test_data/sample/sample_short.shp --element_pth test_data/element/element_short.shp --suti_pth test_data/suiti_result/suiti_result_short.shp --qual_pth test_data/quality_result/quality_short.shp --type_list "['JSBG_7','JSBG_8','TRSX_111','QUAL_76_78','QUAL_77','QUAL_72','QUAL_73','QUAL_74','QUAL_75','SUITI']" -->