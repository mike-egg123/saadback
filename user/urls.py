from django.urls import path
from .views import Users, Personality

urlpatterns = [
    path('getstatus', Users.get_status),  # 获取登录状态
    path('login', Users.login_user),  # 登录
    path('getvalidcode', Users.get_valid_img),  # 获取验证码
    path('logout', Users.logout_user),  # 注销
    path('register', Users.register),  # 注册
    path('change', Personality.change_personality),  # 修改用户信息
    path('change_avatar', Personality.change_avatar),  # 修改用户头像
    path('get', Personality.get_personality),  # 得到用户信息
    path('get_other', Personality.get_personality_other),  # 得到他人信息
    path('modifypassword', Users.modify_password),  # 修改密码
    path('change_follow_state', Users.follow),  # 切换关注状态
    path('getfolloweds', Users.getfolloweds),  # 获取当前用户关注的所有用户
    path('get_follow_state', Users.get_follow_state),  # 请求关注状态，即当前用户是否关注了目标用户
    path('get_userid_by_authorid', Users.get_userid_by_authorid),  # 根据门户id寻找用户id
    path('star_paper', Users.star_paper),  # 收藏学术成果（切换状态）
    path('get_star_paper_by_userid', Users.get_star_paper_by_userid),  # 根据用户id获取收藏学术成果列表
    path('get_star_status', Users.get_star_status),  # 获取收藏状态
    path('get_authorid_by_userid', Users.get_authorid_by_userid),  # 根据用户id寻找门户id

]