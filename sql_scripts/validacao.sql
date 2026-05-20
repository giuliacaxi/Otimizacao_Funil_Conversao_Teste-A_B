WITH sessoes_limpas AS(
	
    SELECT DISTINCT * FROM sessoes

),

metricas_por_variante AS (

	SELECT
		u.variante_escolhida,
        COUNT(DISTINCT u.id_usuario) AS total_usuarios,
        COUNT(s.id_sessao) AS total_sessoes,
        SUM(s.conversao) AS total_conversoes,
        SUM(s.valor_gasto) AS receita_total
	FROM usuarios u
    LEFT JOIN sessoes_limpas s ON u.id_usuario = s.id_usuario
    GROUP BY u.variante_escolhida

)

SELECT
	variante_escolhida,
    total_usuarios,
    total_sessoes,
    total_conversoes,
    receita_total,
    round((total_conversoes / total_sessoes) * 100, 2) AS taxa_conversao,
    round((receita_total / total_usuarios), 2) AS receita_por_usuario
FROM metricas_por_variante