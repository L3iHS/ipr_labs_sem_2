{{- define "postgres-infra.name" -}}
postgres
{{- end -}}

{{- define "postgres-infra.labels" -}}
app.kubernetes.io/name: {{ include "postgres-infra.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{- define "postgres-infra.namespace" -}}
{{- default .Release.Namespace .Values.namespaceOverride -}}
{{- end -}}
