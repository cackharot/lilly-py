#!/usr/bin/env python

import os
import sys
import copy
from inspect import getmembers, isfunction, getmodule
from jinja2 import Environment
import yaml
from helper import data_merge

j2_env = Environment(trim_blocks=True)

def deploy(args):
    if len(args) != 2:
        print("Invalid arguments. deploy <stack> <env>")
        return False
    stack,env = args[0],args[1]

    print("Deploying %s on environment %s" % (stack,env))

    stack_path = os.path.join('./deploy_config',stack,'stack.yaml')
    if not os.path.exists(stack_path):
        print("Invalid stack name! Not found")
        return False

    content = yaml.load(open(stack_path).read())
    gen_namespace(stack,env)

    content = merge_env_content(stack, env, content)
    content['sys_env'] = os.environ

    if 'app_spec' not in content:
        print('No applications found!')
        return True
    for app in content['app_spec']:
        data = app
        app_name = data['name']
        data['stack'] = stack
        data['env'] = env
        data['sys_env'] = content['sys_env']
        for k,v in content['common'].items():
            data[k] = v

        gen_deployment(stack,env,app_name,data)
        gen_service(stack,env,app_name,data)

    return True

def merge_env_content(stack,env,default):
    stack_path = os.path.join('./deploy_config',stack,env,'stack.yaml')
    if not os.path.exists(stack_path):
        return default
    env_content = yaml.load(open(stack_path).read())
    d = copy.deepcopy(default)
    app_spec = d['app_spec']
    d['app_spec'] = []
    cnt = 0
    for app in app_spec:
        data_merge(app,env_content['app_spec'][cnt])
        d['app_spec'].append(app)
        cnt = cnt + 1
    del env_content['app_spec']
    data_merge(d, env_content)
    # print(d)
    return d

def gen_namespace(stack,env):
    data = { 'stack': stack, 'env': env }
    tpl = open(os.path.join('./kube_templates',"namespace.yaml.tpl")).read()
    fc = j2_env.from_string(tpl).render(**data)
    dest_file = os.path.join('./output',stack,env,"%s-ns.yaml" % (stack))
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    open(dest_file, 'w').write(fc)
    return True


def gen_service(stack,env,app_name,data):
    tpl = open(os.path.join('./kube_templates',"service.yaml.tpl")).read()
    fc = j2_env.from_string(tpl).render(**data)
    # print(fc)
    dest_file = os.path.join('./output',stack,env,"%s-svc.yaml" % (app_name))
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    open(dest_file, 'w').write(fc)
    return True

def gen_deployment(stack,env,app_name,data):
    tpl = open(os.path.join('./kube_templates',"deployment.yaml.tpl")).read()
    fc = j2_env.from_string(tpl).render(**data)
    # print(fc)
    dest_file = os.path.join('./output',stack,env,"%s-deployment.yaml" % (app_name))
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    open(dest_file, 'w').write(fc)
    return True

current_module = sys.modules[__name__]
functions_list = [o for o in getmembers(current_module) if isfunction(o[1]) and getmodule(o[1]) == current_module]

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: %s <action> <parameters>" % (sys.argv[0]))
        sys.exit(1)
    action = sys.argv[1]
    action_kv = {}
    for k,v in functions_list:
        action_kv[k] = v
    action_names = action_kv.keys()
    if action not in action_names:
        print("'%s' action not available" % action)
        print("Available actions are %s" % ', '.join(action_names))
        sys.exit(1)

    rem_args = sys.argv[2:]
    ret = action_kv[action](rem_args)
    sys.exit(int(ret))
