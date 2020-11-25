import json
import os
import random
import re

from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse

from .forms import ProfileForm
# 载入数据模型Profile
from .models import Profile


# Create your views here.
class Users:
    # 获取用户登录状态
    @staticmethod
    def get_status(request):
        if request.user.is_authenticated:
            user_id = int(request.user.id)
            if Profile.objects.filter(user_id=user_id).exists():
                userprofile = Profile.objects.get(user_id=user_id)
            else:
                userprofile = Profile.objects.create(user_id=user_id)
            if userprofile.avatar and hasattr(userprofile.avatar, 'url'):
                avatar = "http://182.92.239.145" + str(userprofile.avatar.url)
            else:
                avatar = ""
            return JsonResponse({
                "status": 0,
                "username": str(request.user),
                "email": str(request.user.email),
                "userid":str(request.user.id),
                "phone":str(userprofile.phone),
                "bio":str(userprofile.bio),
                "avatar": avatar
            })
        else:
            return JsonResponse({
                "status": 1
            })

    # 登录
    @staticmethod
    def login_user(request):
        if request.method == "POST":
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            print(password)
            if username is not None and password is not None:
                islogin = authenticate(request, username=username, password=password)
                if islogin:
                    user_id = islogin.id
                    login(request, islogin)
                    if Profile.objects.filter(user_id=user_id).exists():
                        userprofile = Profile.objects.get(user_id=user_id)
                    else:
                        userprofile = Profile.objects.create(user_id=user_id)
                    if userprofile.avatar and hasattr(userprofile.avatar, 'url'):
                        avatar = "http://182.92.239.145" + str(userprofile.avatar.url)
                    else:
                        avatar = ""
                    return JsonResponse({
                        "status": 0,
                        "message": "Login Success",
                        "username": username,
                        "password":password,
                        "email": str(request.user.email),
                        "userid": str(request.user.id),
                        "phone": str(userprofile.phone),
                        "bio": str(userprofile.bio),
                        "avatar": avatar
                    })
                else:
                    return JsonResponse({
                        "status": 1,
                        "message": "登录失败, 请检查用户名或者密码是否输入正确."
                    })
            else:
                return JsonResponse({
                    "status": 2,
                    "message": "参数错误"
                })
        else:
            return JsonResponse({
                "status":3,
                "message":"error method"
            })

    # 注销
    @staticmethod
    def logout_user(request):
        logout(request)
        return JsonResponse({
            "status": 0
        })

    # 注册
    @staticmethod
    def register(request):
        if request.method == "POST":
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            email = data.get("email")
            if username is not None and password is not None and email is not None:
                try:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    login_user = authenticate(request, username=username, password=password)
                    if login_user:
                        login(request, login_user)
                        print(1)
                        return JsonResponse({
                            "status": 0,
                            "userid":user.id,
                            "message": "Register and Login Success"
                        })

                except:
                    print(2)
                    return JsonResponse({
                        "status": 2,
                        "message": "注册失败, 该用户名已经存在."
                    })

        else:
            print(3)
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })
    # 获取验证码
    @staticmethod
    # 获取验证码图片的视图
    def get_valid_img(request):
        # 获取随机颜色的函数
        def get_random_color():
            return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

        # 生成一个图片对象
        img_obj = Image.new(
            'RGB',
            (220, 35),
            get_random_color()
        )
        # 在生成的图片上写字符
        font = ImageFont.truetype('arial.ttf', 30)
        # 生成一个图片画笔对象
        draw_obj = ImageDraw.Draw(img_obj)
        # 开始生成随机字符串并且写到图片上
        tmp_list = []
        for i in range(4):
            u = chr(random.randint(65, 90))  # 生成大写字母
            l = chr(random.randint(97, 122))  # 生成小写字母
            n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

            tmp = random.choice([u, l, n])
            tmp_list.append(tmp)
            draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color(), font = font)

        print(tmp_list)
        mystr = ""
        for s in tmp_list:
            mystr += s
        # 加干扰线
        width = 220  # 图片宽度（防止越界）
        height = 35
        for i in range(4):
            x1 = random.randint(0, width)
            x2 = random.randint(0, width)
            y1 = random.randint(0, height)
            y2 = random.randint(0, height)
            draw_obj.line((x1, y1, x2, y2), fill=get_random_color())

        # 加干扰点
        for i in range(40):
            draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ '/media/checkcode/{}.png'.format(mystr),'wb') as f:
            img_obj.save(f, format = 'png')
        return JsonResponse({
            "url":"http://182.92.239.145" + '/media/checkcode/{}.png'.format(mystr),
            "code":mystr
        })

class Personality:
    # 修改与完善用户信息
    @staticmethod
    def change_personality(request):
        print(request.FILES)
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, request.FILES)
            print(profile_form)
            if profile_form.is_valid():
                profile_cd = profile_form.cleaned_data
                print(profile_cd['phone'])
                print(profile_cd['avatar'])
                print(profile_cd['bio'])
                print(profile_cd['userid'])
                id = int(profile_cd['userid'])
                user = User.objects.get(id=id)
                # profile = Profile.objects.get(user_id = id)
                if Profile.objects.filter(user_id=id).exists():
                    profile = Profile.objects.get(user_id=id)
                else:
                    profile = Profile.objects.create(user=user)
                phone = profile_cd['phone']
                bio = profile_cd['bio']
                if 'avatar' in request.FILES:
                    avatar = profile_cd['avatar']
                # 验证修改数据者是否为用户本人
                else:
                    avatar = profile.avatar
                if False:
                    return JsonResponse({
                        "status":1,
                        "message":"你没有权限修改这个用户的信息"
                    })
                else:
                    profile.phone = phone
                    profile.bio = bio
                    profile.avatar = avatar
                    profile.save()
                    print(1)
                    return JsonResponse({
                        "status":0,
                        "message":"修改成功！"
                    })
            else:
                print(3)
                return JsonResponse({
                    "status":3,
                    "message":"表格数据不合法"
                })
        else:
            print(2)
            return JsonResponse({
                "status":2,
                "message":"请使用post请求"
            })

    # 查看用户信息
    @staticmethod
    def get_personality(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            user_id = data.get('userid')
            user = User.objects.get(id=user_id)
            # userprofile = Profile.objects.get(user_id = user_id)
            if Profile.objects.filter(user_id = user_id).exists():
                userprofile = Profile.objects.get(user_id=user_id)
            else:
                userprofile = Profile.objects.create(user_id = user_id)
            if userprofile.avatar and hasattr(userprofile.avatar, 'url'):
                avatar = "http://182.92.239.145" + str(userprofile.avatar.url)
            else:
                avatar = ""
            username = user.username
            email = user.email
            phone = userprofile.phone
            bio = userprofile.bio
            return JsonResponse({
                "status":0,
                "username":username,
                "email":email,
                "phone":phone,
                "bio":bio,
                "avatar":avatar,
                "userid":user_id
            })
        else:
            return JsonResponse({
                "status":1,
                "message":"请使用post请求"
            })

    # 全局搜索用户
    @staticmethod
    def searchuser(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            keyword = data.get('keyword')
            users = User.objects.all()
            json_list = []
            for user in users:
                username = user.username
                if re.search(keyword, username):
                    json_dict = {}
                    json_dict['userid'] = str(user.id)
                    json_dict['username'] = username
                    profile = Profile.objects.get(user = user)
                    json_dict['avatar'] = "http://182.92.239.145" + str(profile.avatar.url)
                    json_list.append(json_dict)
            return JsonResponse(json_list, safe = False)
        else:
            return JsonResponse({
                "message":"error method"
            })
