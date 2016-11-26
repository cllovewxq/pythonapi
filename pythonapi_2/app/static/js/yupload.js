jQuery.fn.extend( {
	yupload : function(config) {
		var def = {
			btnText		: '浏览...',		//按钮的文本
			accept		: '*',				//选择的文件类型
			maxSize		: 1024*1024 ,		//单个文件大小
			multiple	: true ,			//是否上传多个文件
			url 		: '',				//提交的地址
			method 		: "POST",			//提交的方式

			onSubmit 	: function(v){},	//提交到制定服务后的回调事件；参数为服务端返回的参数
			onSelect	: function(l){},	//选择文件后触发的事件；参数为选择的文件列表
			onUpload 	: function(p){},	//上传文件时，出发的事件；参数为当前的进度
		}
		config = $.extend({},def, config);
		/* ============变量============ */
		var $this = $(this);
		var PENDING_FILES = [];	//文件列表
		var $file 	= document.createElement("input"),
			$btn 	= document.createElement("input");
		/* ============自定义方法============ */
		var setStyle = function(){
			$this.addClass("file-box");

			$file.type 		= 'file';
			$file.accept	= config.accept;
			$file.className = "file-file";
			if(config.multiple) $file.setAttribute("multiple", "multiple");

			$btn.type 		= "button";
			$btn.className 	= "file-btn";
			$btn.value 		= config.btnText;

			$this.append($file);
			$this.append($btn);
		},
		loadEvent = function(){
			var maxsize = config.maxSize;
			$file.onchange = function(){
				var files = this.files;
		        for (var i = 0, ie = files.length ,item; i < ie; i++) {
		        	item = files[i];
		        	// 在这里做验证
		        	if(item.size > maxsize){
		        		alert('大小超过配置的最大值！\n当前大小为：'+item.size+'\n要求的最大值为：'+maxsize);
		        		return;
		        	}
			        PENDING_FILES.push(item);
			    }
			    config.onSelect(files);
			}
		},
		//提交上传
		submitUpload = function(){
			if(!config.url){
				config.onSubmit({error:'提交的URL地址错误'});
				return;
			}
			var param = new FormData();
			// 绑定参数
		    for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
		        param.append("file", PENDING_FILES[i]);
		    }
			var xhr = $.ajax({
		        xhr: function() {
		            var xhrobj = $.ajaxSettings.xhr();
		            if (xhrobj.upload) {
		                xhrobj.upload.addEventListener("progress", function(event) {
		                    var percent = 0;
		                    var position = event.loaded || event.position;
		                    var total    = event.total;
		                    if (event.lengthComputable) {
		                        percent = Math.ceil(position / total * 100);
		                    }
		                    config.onUpload(percent);
		                }, false)
		            }
		            return xhrobj;
		        },
		        url: config.url,
		        method: config.method,
		        contentType: false,
		        processData: false,
		        data: param,
		        success: function(data, textStatus) {config.onSubmit(data); } ,
		        error  : function(XMLHttpRequest, textStatus, errorThrown){
		        	config.onSubmit({error:XMLHttpRequest});
		        	return;
		        }
		    });
		}
		setStyle();
		loadEvent();
		return {
			submitUpload : submitUpload ,
			getFiles	 : PENDING_FILES,
		}
	}
});

