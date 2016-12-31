apiVersion: v1
kind: Service
metadata:
  name: {{stack}}-{{name}}-svc
  namespace: {{stack}}-{{env}}
  labels:
    name: {{stack}}-{{name}}-svc
spec:
  selector:
    app: {{stack}}-{{name}}
  type: LoadBalancer
  ports:
  - name: http
    targetPort: {{ports[0]}}
    port: {{service_port | default('80')}}
    protocol: TCP
