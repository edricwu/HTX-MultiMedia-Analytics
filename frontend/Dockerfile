# =========================
# 1. Base Build Stage (with DOCKER arg passed for next.config)
# =========================
FROM node:20.11.1 AS base
WORKDIR /app

ARG DOCKER
ENV DOCKER=${DOCKER}

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build


# =========================
# 2. Production Stage (used by main frontend)
# =========================
FROM node:20.11.1-slim AS production
WORKDIR /app

COPY --from=base /app /app
RUN npm install --omit=dev

EXPOSE 3000
CMD ["npm", "start"]


# =========================
# 3. Test Stage (used by frontend-tests)
# =========================
FROM base AS test
WORKDIR /app
CMD ["npm", "test", "--", "--watchAll=false"]
