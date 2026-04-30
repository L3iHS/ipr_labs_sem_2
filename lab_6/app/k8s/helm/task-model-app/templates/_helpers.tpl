{{- define "task-model-app.name" -}}
task-model
{{- end -}}

{{- define "task-model-app.labels" -}}
app.kubernetes.io/name: {{ include "task-model-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{- define "task-model-app.namespace" -}}
{{- default .Release.Namespace .Values.namespaceOverride -}}
{{- end -}}
