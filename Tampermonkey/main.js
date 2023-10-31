// ==UserScript==
// @name         AAM的qb扩展脚本
// @namespace    http://tampermonkey.net/
// @version      0.1.1
// @description  I want sleep I sole want sleep a nd I like sleep
// @author       github/Abcuders
// @supportURL   https://github.com/Abcuders/AutoAnimeMv
// @match        https://mikanani.me/*
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_registerMenuCommand
// @grant        GM_getResourceURL
// @grant        GM_getResourceText
// @grant        GM_addStyle
// @grant        GM_xmlhttpRequest
// @connect      *
// @require      https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.2/jquery-confirm.min.js
// @resource css https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.2/jquery-confirm.min.css
// @icon         https://mikanani.me/images/mikan-pic.png
// ==/UserScript==

function updata(){
    var item = document.querySelectorAll('.js-magnet');
    for (var i=0;i<item.length;i++)
    {
        let URL = $(item[i]).attr('data-clipboard-text');
        //console.log(item[i].parentElement);
        var a = document.createElement('a');
        //a.className = 'btn logmod-submit js-subscribe_bangumi_page';
        a.className = 'js-magnet magnet-link';
        a.innerText = '[发送给qB下载]';
        //a.style.width = '55px';
        //a.style.height = '35px';
        a.onclick = function(){
        ToQBDownload(URL);
        };
        item[i].parentElement.appendChild(a);
   }
   function ToQBDownload(URL){
        if (!GM_getValue('address')){
            $.alert({title: 'Erorr!',content: '您还没有配置脚本',type: 'red'});
            return false;
        }
        let formData = new FormData();
        formData.append('urls', URL);
        formData.append('autoTMM', true); // 自动
        //formData.append('savepath', config.savePath);
        //formData.append('cookie', '');
        //formData.append('rename', rename);
        formData.append('category', '动漫');
        //formData.append('paused', config.paused);
        //formData.append('stopCondition', 'None');
        //formData.append('contentLayout', 'Original');
        //formData.append('dlLimit', 'NaN');
        //formData.append('upLimit', 'NaN');
        GM_xmlhttpRequest({
            method: 'post',
            url: `http://${GM_getValue('address')}/api/v2/torrents/add`,
            data: formData,
            onload: function(rec) {
                console.log(rec);
                if (rec.status == 403){
                    if (rec.response == 'Forbidden'){
                       GM_xmlhttpRequest({
                           method: 'post',
                           url: `http://${GM_getValue('address')}/api/v2/auth/login`,
                           data: `username=${GM_getValue('username')}&password=${GM_getValue('password')}`,
                           headers: {"Content-Type": "application/x-www-form-urlencoded"},
                           onload: function(rec) {
                               console.log(rec);
                               console.log(URL);
                               ToQBDownload(URL);
                           }
                       });
                    }
                }else if (rec.status == 200){
                    $.alert('添加成功');
                }else{
                    $.alert('添加失败');
                }
            },
            timeout:5000,
            ontimeout: function(){
                $.slert('连接超时');
            }
        });
    }
}

function OpenConfig(){
    $.confirm({
        title: 'AAM油猴脚本相关配置',
        theme: 'light',
        type: 'orange',
        animation: 'rotateX',
        closeAnimation: 'rotateX',
        animateFromElement: false,
        content: '' +
        '<form action="" class="formName">' +
        '<div class="form-group">' +
        '<label>qb服务器地址</label>' +
        `<input type="text" placeholder="如 192.168.1.1:8080" value="${GM_getValue('address')}" class="address form-control" required />` +
        '<label>UserName</label>' +
        `<input type="text" placeholder="username" value="${GM_getValue('username')}" class="username form-control" required />` +
        '<label>Password</label>' +
        `<input type="text" placeholder="password" value="${GM_getValue('password')}" class="password form-control" required />` +
        '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: '完成',
                btnClass: 'btn-blue',
                action: function () {
                    let address = this.$content.find('.address').val();
                    let username = this.$content.find('.username').val();
                    let password = this.$content.find('.password').val();
                    if(!address || !username || !password){
                        $.alert('配置不能为空');
                        return false;
                    }
                    GM_setValue('address',address); // qBittorrent Web UI 地址 http://127.0.0.1:8080
                    GM_setValue('username',username); // qBittorrent Web UI的用户名
                    GM_setValue('password',password); // qBittorrent Web UI的密码
                }
            },
            test: {
                text: '测试',
                btnClass: 'btn-success',
                action: function () {
                    var address = this.$content.find('.address').val();
                    var username = this.$content.find('.username').val();
                    var password = this.$content.find('.password').val();
                    if(!address || !username || !password){
                        $.alert('配置不能为空');
                        return false;
                    }
                    GM_xmlhttpRequest({
                        method: 'post',
                        url: `http://${address}/api/v2/auth/login`,
                        data: `username=${username}&password=${password}`,
                        headers: {"Content-Type": "application/x-www-form-urlencoded"},
                        onload: function(rec) {
                            console.log(rec);
                            if (rec.responseText == 'Ok.'){
                                $.alert('测试通过');
                                //var Cookie = rec.responseHeaders
                            }else if (rec.responseText == 'Fails.'){
                                $.alert('帐户或密码错误');
                            }else{
                                $.alert('？');
                            }
                        },
                        timeout:5000,
                        ontimeout: function(){
                            $.slert('连接超时');
                        }
                    });
                    return false;
                }
            },
            cancel: function () {
                //close
            },
        },
        onContentReady: function () {
            // bind to events
            var jc = this;
            this.$content.find('form').on('submit', function (e) {
                // if the user submits the form by pressing enter in the field.
                e.preventDefault();
                jc.$$formSubmit.trigger('click'); // reference the button and click it
            });
        }
    });
}

GM_addStyle(GM_getResourceText("css"));
GM_registerMenuCommand('配置qb信息',OpenConfig,'h');
if (!GM_getValue("address") || !GM_getValue("username") || !GM_getValue("password")){
    $.alert({
        title: '欢迎使用AAM油猴脚本!',
        theme: 'supervan',
        content: '接下来请配置脚本的相关内容',
    });
    GM_setValue('address','');
    GM_setValue('username','');
    GM_setValue('password','');
}
updata();
