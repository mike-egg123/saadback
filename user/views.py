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
from .models import Profile, Follow, StarPaper
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

prefix = "http://49.234.51.41"


class CustomBackend(ModelBackend):
    """邮箱也能登录"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


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
                avatar = prefix + str(userprofile.avatar.url)
            else:
                avatar = ""
            return JsonResponse({
                "status": 0,
                "username": str(request.user),
                "email": str(request.user.email),
                "userid":request.user.id,
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
                        avatar = prefix + str(userprofile.avatar.url)
                    else:
                        avatar = ""
                    return JsonResponse({
                        "status": 0,
                        "message": "Login Success",
                        "username": username,
                        "password": password,
                        "email": str(request.user.email),
                        "userid": request.user.id,
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
            if User.objects.filter(email=email):
                return JsonResponse({
                    "status": 2,
                    "message": "注册失败, 该邮箱已经存在."
                })
            if username is not None and password is not None and email is not None:
                try:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    login_user = authenticate(request, username=username, password=password)
                    if login_user:
                        login(request, login_user)
                        print(1)
                        profile = Profile.objects.create(user=user)
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
    # 修改密码
    @staticmethod
    def modify_password(request):
        # 要验证一下当前的密码
        if request.method == "POST":
            data = json.loads(request.body)
            oldpassword = data.get("oldpassword")
            user = request.user
            username = user.username
            # print(password)
            if oldpassword is not None:
                islogin = authenticate(request, username=username, password=oldpassword)
                if islogin:
                    user_id = islogin.id
                    newpassword = data.get("newpassword")
                    newpassword2 = data.get("newpassword2")
                    if newpassword == newpassword2:
                        user.set_password(newpassword)
                        user.save()
                        return JsonResponse({
                            "status":0,
                            "message":"修改成功"
                        })
                    else:
                        return JsonResponse({
                            "status": 1,
                            "message": "两次新密码不一致"
                        })
                else:
                    return JsonResponse({
                        "status": 2,
                        "message": "原密码不正确"
                    })
    # 切换关注的状态
    @staticmethod
    def follow(request):
        if request.method == "POST":
            data = json.loads(request.body)
            followed_id = data.get("userid")
            follower_id = request.user.id
            try:
                follow = Follow.objects.get(follower_id = follower_id, followed_id = followed_id)
            except Exception as e:
                try:
                    follow = Follow.objects.create(follower_id=follower_id, followed_id=followed_id)
                except Exception as e:
                    return JsonResponse({
                        "status": 2,
                        "message": "此用户不存在"
                    })
                else:
                    follow.save()
                    return JsonResponse({
                        "status": 0,
                        "message": "关注成功"
                    })
            else:
                follow.delete()
                return JsonResponse({
                    "status": 0,
                    "message": "取消关注成功"
                })
        else:
            return JsonResponse({
                "status":1,
                "message":"请求方式有误"
            })
    #获取关注的所有用户
    @staticmethod
    def getfolloweds(request):
        if request.method == "POST":
            follower_id = request.user.id
            try:
                followeds = Follow.objects.filter(follower_id=follower_id)
            except Exception as e:
                return JsonResponse({
                    "status":2,
                    "message":"该用户不存在"
                })
            else:
                followeds_list = []
                for followed in followeds:
                    followed_dic = {}
                    userid = followed.followed_id
                    followed_dic['userid'] = userid
                    profile = Profile.objects.get(user_id=userid)
                    followed_dic['ava_url'] = str(profile.avatar)
                    followed_dic['org'] = profile.org
                    followed_dic['pos'] = profile.position
                    user = User.objects.get(id=userid)
                    followed_dic['email'] = user.email
                    followeds_list.append(followed_dic)
                # followeds_json = json.dump(followeds_list)
                return JsonResponse({
                    "status":0,
                    "f_list":followeds_list
                })
        else:
            return JsonResponse({
                "status": 1,
                "message": "请求方式有误"
            })

    # 获取当前用户对目标用户的关注状态
    @staticmethod
    def get_follow_state(request):
        if request.method == "POST":
            data = json.loads(request.body)
            followed_id = data.get('userid')
            follower_id = request.user.id
            try:
                follow = Follow.objects.get(follower_id = follower_id, followed_id = followed_id)
            except Exception as e:
                return JsonResponse({
                    "status": 0,
                    "is_follow": False
                })
            else:
                return JsonResponse({
                    "status": 0,
                    "is_follow": True
                })
        else:
            return JsonResponse({
                "status": 1,
                "message": "请求方式有误"
            })

    # 根据传入的门户id寻找用户id
    @staticmethod
    def get_userid_by_authorid(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            authorid = data.get('authorid')
            try:
                profile = Profile.objects.get(author_id = authorid)
            except Exception as e:
                return JsonResponse({
                    "status":0,
                    "userid":-1
                })
            else:
                return JsonResponse({
                    "status":0,
                    "userid":profile.user_id
                })
        else:
            return JsonResponse({
                "status":1,
                "message":"请求方式有误"
            })

    # 根据传入的用户id寻找门户id
    @staticmethod
    def get_authorid_by_userid(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            userid = data.get('userid')
            try:
                profile = Profile.objects.get(user_id=userid)
            except Exception as e:
                return JsonResponse({
                    "status": 0,
                    "authorid": -1
                })
            else:
                return JsonResponse({
                    "status": 0,
                    "authorid": profile.author_id
                })
        else:
            return JsonResponse({
                "status": 1,
                "message": "请求方式有误"
            })

    # 收藏学术成果
    @staticmethod
    def star_paper(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            userid = data.get('userid')
            paperid = data.get('paperid')
            if StarPaper.objects.filter(user_id=userid, paper_id=paperid).exists():
                starpapers = StarPaper.objects.filter(user_id=userid, paper_id=paperid)
                for starpaper in starpapers:
                    starpaper.delete()
                return JsonResponse({
                    "status":0,
                    "message":"取消收藏！"
                })
            else:
                starpaper = StarPaper.objects.create(user_id=userid, paper_id=paperid)
                starpaper.save()
                return JsonResponse({
                    "status": 0,
                    "message": "收藏成功！"
                })

        else:
            return JsonResponse({
                "status": 1,
                "message": "请求方式有误"
            })

    # 根据用户id获取收藏学术成果列表
    @staticmethod
    def get_star_paper_by_userid(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            userid = data.get("userid")
            star_paper_list = []
            if StarPaper.objects.filter(user_id=userid).exists():
                starpapers = StarPaper.objects.filter(user_id=userid)
                for starpaper in starpapers:
                    id = starpaper.paper_id
                    star_paper_list.append(id)
                return JsonResponse({
                    "status":0,
                    "paper_id_list":star_paper_list
                })
            else:
                return JsonResponse({
                    "status":0,
                    "paper_id_list":star_paper_list
                })
        else:
            return JsonResponse({
                "status":1,
                "message":"请求方式有误"
            })


    # 获取收藏状态
    @staticmethod
    def get_star_status(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            userid = data.get('userid')
            paperid = data.get('paperid')
            if StarPaper.objects.filter(user_id=userid, paper_id=paperid).exists():
                return JsonResponse({
                    "status":0,
                    "is_star":True
                })
            else:
                return JsonResponse({
                    "status": 0,
                    "is_star": False
                })
        else:
            return JsonResponse({
                "status": 1,
                "message": "请求方式有误"
            })

class Personality:
    # 修改与完善用户信息
    @staticmethod
    def change_personality(request):
        print(request.FILES)
        if request.method == 'POST':
            data = json.loads(request.body)
            id = request.user.id
            user = User.objects.get(id=id)
            # profile = Profile.objects.get(user_id = id)
            if Profile.objects.filter(user_id=id).exists():
                profile = Profile.objects.get(user_id=id)
            else:
                profile = Profile.objects.create(user=user)
            phone = data.get("phone")
            bio = data.get("bio")
            profile.phone = phone
            profile.bio = bio
            profile.org = data.get("org")
            profile.position = data.get("position")
            profile.gender = data.get("gender")
            profile.save()
            print(1)
            return JsonResponse({
                "status":0,
                "message":"修改成功！"
            })
        else:
            print(2)
            return JsonResponse({
                "status":2,
                "message":"请使用post请求"
            })

    # 修改用户头像
    @staticmethod
    def change_avatar(request):
        print(request.FILES)
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, request.FILES)
            if profile_form.is_valid():
                profile_cd = profile_form.cleaned_data
                print(profile_cd['avatar'])
                id = request.user.id
                user = User.objects.get(id=id)
                # profile = Profile.objects.get(user_id = id)
                if Profile.objects.filter(user_id=id).exists():
                    profile = Profile.objects.get(user_id=id)
                else:
                    profile = Profile.objects.create(user=user)
                if 'avatar' in request.FILES:
                    avatar = profile_cd['avatar']
                else:
                    avatar = profile.avatar
                profile.avatar = avatar
                profile.save()
                return JsonResponse({
                    "status": 0,
                    "message": "修改成功！"
                })
            else:
                print(3)
                return JsonResponse({
                    "status": 3,
                    "message": "表格数据不合法"
                })
        else:
            print(2)
            return JsonResponse({
                "status": 2,
                "message": "请使用post请求"
            })

    # 查看用户信息
    @staticmethod
    def get_personality(request):
        if request.method == 'POST':
            # data = json.loads(request.body)
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            # userprofile = Profile.objects.get(user_id = user_id)
            if Profile.objects.filter(user_id = user_id).exists():
                userprofile = Profile.objects.get(user_id=user_id)
            else:
                userprofile = Profile.objects.create(user_id = user_id)
            if userprofile.avatar and hasattr(userprofile.avatar, 'url'):
                avatar = prefix + str(userprofile.avatar.url)
            else:
                avatar = ""
            username = user.username
            email = user.email
            phone = userprofile.phone
            bio = userprofile.bio
            birthday = userprofile.birthday
            addr = userprofile.address
            org = userprofile.org
            postion = userprofile.position
            gender = userprofile.gender
            is_administrator = userprofile.is_administrator
            is_associated = userprofile.is_associated
            author_id = userprofile.author_id
            realname = userprofile.realname
            return JsonResponse({
                "status":0,
                "username":username,
                "email":email,
                "phone":phone,
                "bio":bio,
                "avatar":avatar,
                "userid":user_id,
                "birthday":birthday,
                "addr":addr,
                "org":org,
                "postion":postion,
                "gender":gender,
                "is_admin":is_administrator,
                "is_associated":is_associated,
                "author_id":author_id,
                "realname":realname
            })
        else:
            return JsonResponse({
                "status":1,
                "message":"请使用post请求"
            })

    # 查看用户信息
    @staticmethod
    def get_personality_other(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            user_id = data.get("userid")
            user = User.objects.get(id=user_id)
            # userprofile = Profile.objects.get(user_id = user_id)
            if Profile.objects.filter(user_id=user_id).exists():
                userprofile = Profile.objects.get(user_id=user_id)
            else:
                userprofile = Profile.objects.create(user_id=user_id)
            if userprofile.avatar and hasattr(userprofile.avatar, 'url'):
                avatar = prefix + str(userprofile.avatar.url)
            else:
                avatar = ""
            username = user.username
            email = user.email
            phone = userprofile.phone
            bio = userprofile.bio
            birthday = userprofile.birthday
            addr = userprofile.address
            org = userprofile.org
            postion = userprofile.position
            gender = userprofile.gender
            is_administrator = userprofile.is_administrator
            is_associated = userprofile.is_associated
            author_id = userprofile.author_id
            realname = userprofile.realname
            return JsonResponse({
                "status": 0,
                "username": username,
                "email": email,
                "phone": phone,
                "bio": bio,
                "avatar": avatar,
                "userid": user_id,
                "birthday": birthday,
                "addr": addr,
                "org": org,
                "postion": postion,
                "gender": gender,
                "is_admin": is_administrator,
                "is_associated": is_associated,
                "author_id": author_id,
                "realname": realname
            })
        else:
            return JsonResponse({
                "status": 1,
                "message": "请使用post请求"
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
                    json_dict['avatar'] = prefix + str(profile.avatar.url)
                    json_list.append(json_dict)
            return JsonResponse(json_list, safe = False)
        else:
            return JsonResponse({
                "message":"error method"
            })
