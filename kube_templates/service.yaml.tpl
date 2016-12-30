apiVersion: v1
kind: Service
metadata:
  name: {{stack}}-{{env}}-{{name}}-svc
  namespace: {{stack}}-{{env}}
  labels:
    app: {{stack}}-{{env}}-{{name}}
spec:
  selector:
    app: {{stack}}-{{env}}-{{name}}
  type: LoadBalancer
  ports:
  - name: http
    targetPort: {{ports[0]}}
    port: {{service_port | default('80')}}
    protocol: TCP
