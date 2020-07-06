# -*- coding: utf-8 -*-
from functools import wraps
 
from django.shortcuts import render_to_response
 
 
def partial(func):
    @wraps(func)
    def wrapper(strategy, pipeline_index, *args, **kwargs):
        out = func(strategy=strategy, pipeline_index=pipeline_index,
                    *args, **kwargs) or {}
        if not isinstance(out, dict):
            values = strategy.partial_to_session(pipeline_index, *args,
                                                 **kwargs)
            strategy.session_set('partial_pipeline', values)
        return out
    return wrapper
 
 
@partial
def optional_user_data(backend, details, response, request, user, is_new=False, *args, **kwargs):
    if backend.name == 'kakao' and is_new:
        data = backend.strategy.request_data()
        if data.get('introduction') is None:
            return render_to_response('accounts/profile_update.html', {'fb_details': details, })
        else:
            return {'introduction': data.get('introduction')}
 
 
def save_profile(backend, user, response, is_new, *args, **kwargs):
    if backend.name == 'kakao' and is_new:
        data = backend.strategy.request_data()
 
        profile = user.profile
        profile.phone = data.get('phone', '')
        profile.email = response.get('email', '')
        profile.name = response.get('name', '')
        profile.sms_receiving_consent = data.get('sms_receiving_consent', '')
        profile.email_receiving_consent = data.get('email_receiving_consent', '')
        profile.save()