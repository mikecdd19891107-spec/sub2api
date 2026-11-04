package service

import (
	"github.com/mikecdd19891107-spec/agentbyte/internal/config"
	"github.com/mikecdd19891107-spec/agentbyte/internal/util/responseheaders"
)

func compileResponseHeaderFilter(cfg *config.Config) *responseheaders.CompiledHeaderFilter {
	if cfg == nil {
		return nil
	}
	return responseheaders.CompileHeaderFilter(cfg.Security.ResponseHeaders)
}
