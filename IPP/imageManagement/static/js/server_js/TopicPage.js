
$(function () {

    //1.init table
    var oTable = new TableInit();
    oTable.Init();

    //2.init table click event
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();

});

var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
         var $table = $('#topic');
        $(function () {
        $table.bootstrapTable({
            url:'/getTopicJsonData' ,
            method: 'get',                      //request method
            toolbar: '#toolbar',                //toolbar container
            striped: true,
            cache: false,                       //enable cache
            pagination: true,                   //enable paging（*）
            sortable: true,                     //enable sorting
            sortOrder: "asc",                   //sorting plan
            sidePagination: "server",           //paging method：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //
            pageSize: 10,                       //rows per page（*）
            pageList: [10, 25, 50, 100],        //（*）
            search: true,                       //search in the chart
            strictSearch: true,
            showColumns: true,
            showRefresh: true,                  //fresh button
            minimumCountColumns: 2,             //
            clickToSelect: false,                //
            height: 500,                        //
            uniqueId: "ID",                     //
            showToggle:false,
            queryParams:oTableInit.queryParams,
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                field: 'id',
                title: 'ID'
            }, {
                field: 'topicName',
                title: 'Topic Name',
                editable:true
            }, {
                field: 'createTime',
                title: 'Create Time'
            }, {
                field: 'lastUpdateTime',
                title: 'Last Update Time'
            }, {
                field: 'trainTimes',
                title: 'Training Times'
            },{
                field: 'note',
                title: 'Description',
                editable:true

            } ],
            onEditableSave: function (field, row, oldValue, $el) {
                $.ajax({
                    type: "post",
                    url: "/modify-topic/",
                    data: {strJson: JSON.stringify(row)},
                    success: function (data, status) {
                        alert(data+status+"success");

                    },
                    error: function () {
                        alert("Topic name already exist!");
                    },
                    complete: function () {

                    }

                })
            }
        });
    });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            topic_name: $("#search_topic_name").val(),
        };
        return temp;
    };
    return oTableInit;
};


var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
    };

    return oInit;
};