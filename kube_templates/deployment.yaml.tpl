apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: {{stack}}-{{name}}
  namespace: {{stack}}-{{env}}
spec:
  replicas: {{replicas}}
  template:
    metadata:
      labels:
    {% for k,v in metadata.items() %}
    {{k}}: {{v}}
    {% endfor -%}
    spec:
      containers:
      - name: {{stack}}-{{name}}
        image: {{registry_url}}/{{image_name}}:{{sys_env['GO_DEPENDENCY_LABEL_BUILD']}}
        env:
        {% for k,v in properties.items() -%}
        - name: {{k}}
          value: {{v}}
        {% endfor -%}
        ports:
        {% for p in ports -%}
        - containerPort: {{p}}
        {% endfor -%}

