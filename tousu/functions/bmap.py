html_base = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>${title}</title>
    <style type="text/css">
        html{height:100%}
        body{height:100%;margin:0px;padding:0px}
        #container{height:100%}
    </style>
</head>
<body>
<div id="container"></div>
</body>
<script type="text/javascript" src="http://api.map.baidu.com/api?v=3.0&ak=gnWSbTKQ3YLGDpVMcefvOQ3YA39UuTC4"></script>
<script type="text/javascript">
	function G(id) {
		return document.getElementById(id);
	}
	//搜索框控件
	// 定义一个控件类，即function
	function SearchControl(){
		// 设置默认停靠位置和偏移量
		this.defaultAnchor = BMAP_ANCHOR_TOP_LEFT;
		this.defaultOffset = new BMap.Size(72, 48);
	}
	// 通过JavaScript的prototype属性继承于BMap.Control
	SearchControl.prototype = new BMap.Control();
	// 自定义控件必须实现initialize方法，并且将控件的DOM元素返回
	// 在本方法中创建个div元素作为控件的容器，并将其添加到地图容器中
	SearchControl.prototype.initialize = function(map){
		var placeMarkers = []
		var searchInput = document.createElement("input");  
		// 创建一个DOM元素
		var div = document.createElement("div");
		// 添加文字说明
		div.appendChild(searchInput);
		div.style.opacity=0.6;
		searchInput.placeholder = '';
		searchInput.style.height = '32px';
		searchInput.style.width = '368px';
		searchInput.style.fontSize = '18px';
		searchInput.style.lineHeight = '32px';
		ac = new BMap.Autocomplete(
			{
				"input" : searchInput, 
				"location" : map
			});
		var myValue;
		ac.addEventListener("onconfirm", function(e) {    //鼠标点击下拉列表后的事件
			var _value = e.item.value;
			myValue = _value.province +  _value.city +  _value.district +  _value.street +  _value.business;
			setPlace();
		});

		function setPlace(){
			for(var idx = 0; idx < placeMarkers.length; idx++){
				map.removeOverlay(placeMarkers[idx]);
			}
			placeMarkers = [];
			function myFun(){
				var pp = local.getResults().getPoi(0).point;    //获取第一个智能搜索的结果
				var overlay = new BMap.Marker(pp);
				placeMarkers.push(overlay);
				map.centerAndZoom(pp, 18);
				map.addOverlay(overlay);    //添加标注
			}
			var local = new BMap.LocalSearch(map, { //智能搜索
				onSearchComplete: myFun
			});
			local.search(myValue);
		}
		map.getContainer().appendChild(div);
		return div;
	}
</script>
<script type="text/javascript">
	var grids = [];
	var workList = [];
	var map = new BMap.Map("container");          // 创建地图实例
	var point = new BMap.Point(102.715025,25.053312);  // 创建点坐标
	map.centerAndZoom(point, 15);                 // 初始化地图，设置中心点坐标和地图级别
	map.enableScrollWheelZoom(true);     //开启鼠标滚轮缩放
	map.addControl(new BMap.NavigationControl());
	map.addControl(new BMap.ScaleControl());
	map.addControl(new BMap.OverviewMapControl());
	map.addControl(new BMap.MapTypeControl());
	map.addControl(new SearchControl());
</script>
</html>
'''


def build_bmap(dst_file, title, grids, work_list):
    html_base.replace('${title}', title)
    with open(dst_file, 'w', encoding='utf8') as out:
        out.write(html_base)